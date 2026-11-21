#!/usr/bin/env bash
# Runs from the clone root before every Tessl cloud run.
#
# Sets up commit signing from the factory environment's GIT_SIGNING_KEY
# secret, so factory runs can follow the rule that every commit is signed.
# The key can be an SSH private key or an armored PGP private key, given
# as-is, with literal \n escapes, or base64-encoded.
#
# GitHub marks a commit verified only when the committer's email belongs to
# the account that holds the key. Set GIT_SIGNING_NAME and GIT_SIGNING_EMAIL
# in the environment to commit as that account.
#
# The key is never printed.
set -eo pipefail

if [[ -z "${GIT_SIGNING_KEY:-}" ]]; then
  echo "GIT_SIGNING_KEY is not set; skipping commit signing setup"
  exit 0
fi

echo "Decoding GIT_SIGNING_KEY"
key="$GIT_SIGNING_KEY"
if [[ "$key" != *"-----BEGIN"* ]]; then
  key="$(printf '%s' "$key" | base64 -d 2>/dev/null || true)"
fi
if [[ "$key" != *$'\n'* ]]; then
  key="$(printf '%b' "$key")"
fi

case "$key" in
  *"-----BEGIN OPENSSH PRIVATE KEY-----"*)
    echo "Configuring SSH commit signing"
    install -d -m 700 "$HOME/.ssh"
    key_file="$HOME/.ssh/git_signing_key"
    (umask 077 && printf '%s\n' "$key" > "$key_file")
    ssh-keygen -y -f "$key_file" > "$key_file.pub"
    git config --global gpg.format ssh
    git config --global user.signingkey "$key_file"
    ;;
  *"-----BEGIN PGP PRIVATE KEY BLOCK-----"*)
    echo "Configuring PGP commit signing"
    printf '%s\n' "$key" | gpg --batch --import 2>/dev/null
    fingerprint="$(gpg --batch --with-colons --list-secret-keys | awk -F: '$1 == "fpr" { print $10; exit }')"
    git config --global gpg.format openpgp
    git config --global user.signingkey "$fingerprint"
    ;;
  *)
    echo "GIT_SIGNING_KEY is neither an OpenSSH nor a PGP private key" >&2
    exit 1
    ;;
esac

git config --global commit.gpgsign true
git config --global tag.gpgsign true

if [[ -n "${GIT_SIGNING_NAME:-}" ]]; then
  echo "Setting committer name"
  git config --global user.name "$GIT_SIGNING_NAME"
fi
if [[ -n "${GIT_SIGNING_EMAIL:-}" ]]; then
  echo "Setting committer email"
  git config --global user.email "$GIT_SIGNING_EMAIL"
fi

echo "Checking that git can sign"
check_dir="$(mktemp -d)"
git -C "$check_dir" init -q
git -C "$check_dir" -c user.name=check -c user.email=check@example.invalid \
  commit -q --allow-empty -m "signing check"
rm -rf "$check_dir"
echo "Commit signing is ready"
