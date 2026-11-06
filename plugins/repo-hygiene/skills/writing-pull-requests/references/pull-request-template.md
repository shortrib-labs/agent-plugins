<!--
PULL REQUEST TEMPLATE (v4)

This template follows a conversational, practitioner-focused style that combines technical
precision with approachable explanations. Write as an experienced developer sharing knowledge
with colleagues—direct and no-nonsense, but not dry or overly formal.

TITLE REQUIREMENTS (ALL must pass):
- Start with verb in third person present tense (e.g., "Adds", "Fixes", "Improves")
- ≤ 40 characters total
- Present tense only (no "Added", "Will add", etc.)
- No first person ("I", "We", "My")
- Focus on INTENT (the business outcome or capability), not implementation details
- Good: "Tracks CMX credit purchases as deals" (what it enables)
- Bad: "Adds webhook handler and event listener" (how it's built)

BODY REQUIREMENTS:
- Use exact markdown headers below (case sensitive, correct dash count). All
  sections, including optional ones, use setext dash underlines, not ATX `##`
  headings.
- TL;DR: 1-2 sentences maximum, start with DIFFERENT verb than title. State
  the intent (what problem gets solved or what becomes possible), not the
  mechanism.
- Closes: issue reference between TL;DR and Details, using "Closes".
- Details: Explain WHY the change was needed, your approach, and its impact.
  Implementation details are in the diff.
- No forbidden phrases: "this PR", "this change", "this commit", "this update"
- Present tense and active voice throughout
- Technical precision: include exact versions, commands, file paths in
  `backticks`

BEFORE SUBMITTING:
- [ ] Title ≤ 40 characters with verb in third person present tense (quick
  test: ends in "s")
- [ ] TL;DR starts with different verb than title, same tense
- [ ] Details opens with a different verb than both the title and TL;DR
- [ ] No banned phrases in body
- [ ] Headers formatted exactly as shown below
- [ ] Details answers "what is this about" and "how do I verify it" — not
  "what will I see in Files Changed"
- [ ] If included, Test plan items are all checked and carry evidence
- [ ] Tests pass
- [ ] Linting passes
-->

<!-- Replace this comment with your title following the requirements above -->

TL;DR
-----
<!-- One or two sentences explaining the intent using a DIFFERENT verb than your title.
     State what problem gets solved or what becomes possible — not how it's built.
     Good: "Gives the revenue team automatic CRM visibility into credit purchases."
     Bad: "Implements a webhook handler that creates deal records via the REST API."
-->

<!-- Reference the issue here. Use "Closes" (not "Fixes" or "Resolves") for
     consistency. Delete the line if there is no issue. -->
Closes #

Details
-------
<!-- Explain WHY this change was needed and its impact. Tell the story behind the change.
     What problem does it solve? What improvement does it enable?

     Write as if answering two questions for the reviewer: "What is this all
     about?" and "How will I know if you did it right?" The diff covers
     implementation — the PR body should not retrace it. A sentence describing
     which CSS class a template uses, which color token the date renders in, or
     which file was renamed belongs in the diff, not here.

     Ground the reader in the reasoning, not the mechanics:
     - Why this needed solving now, or what it unblocks going forward
     - Why this approach over alternatives you considered or rejected
     - What tradeoffs, constraints, or limitations shaped the decision (be honest)
     - What existing patterns or conventions this follows
     - Links to relevant documentation or issues

     If there are novel, clever, or tricky ideas in the code, mention those
     fragments in the PR text. You may quote snippets of the code to explain
     these areas. You may use small code blocks for these types of details
     ONLY.

     Version numbers, commands, identifiers, and file paths should be in
     `backticks`.

     Use active voice and third person present tense throughout. Try to avoid
     bullet points and lists. This is a narrative to assist the reviewer and is
     the start of a conversation with them.

     FIRST SENTENCE GUIDANCE: The first sentence always has the PR as its
     implied subject and starts with a DIFFERENT verb than the TL;DR or PR
     title.

     SUBJECT GUIDANCE: Start sentences with either (1) an implied subject
     (the PR itself): "Creates a bucket with versioning disabled..." or
     (2) a concrete subject (actual infrastructure): "The bucket disables
     versioning since..." Avoid vague stand-ins like "the solution",
     "the change", "this PR"—these are just dressed-up ways of referring
     to the work itself and violate the "no forbidden phrases" rule.

     End with a verification step: a URL to visit, a command to run, or a
     behavior to observe that confirms the work is correct.
-->

<!-- Optional sections: add any that apply, using a setext heading (dash
     underline the same length as the heading text), like TL;DR and Details.

     Test plan
     ---------
     Describe what was tested and the result, not what will be tested.
     Every item uses - [x] (verified), never - [ ] (unchecked). Include
     concrete evidence: command output, record counts, HTTP status codes,
     test suite pass counts.

     Breaking Changes
     ----------------
     List any breaking changes and migration steps.

     Dependencies
     ------------
     Note any new dependencies or version updates.
-->
