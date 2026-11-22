Here are my notes from yesterday. Turn them into my standup for the team channel, ready to send. Save it to `standup.md`.

- debugged flaky `payments-api` integration tests, root cause was a shared Postgres fixture, fixed it, CI green again, 3 reruns before that
- met with Dana from Finance about invoice export, she needs CSV by Friday
- reviewed 4 PRs
- started the day triaging Sentry, 31 new errors, 28 were the same retry bug
- shipped retry backoff fix to production at 4pm
- paired with Omar on the Kafka consumer lag dashboard, not finished
