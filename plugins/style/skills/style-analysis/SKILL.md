---
name: style-analysis
description: Analyzes writing samples to work out how someone writes and produces an installable voice skill from them. Use when given a person's or publication's past writing and asked to capture, describe or document the voice. Not for judging or editing prose quality; that is the taste skill.
---

# Style Analysis

A method for analyzing text and producing comprehensive writing style guides. This is the meta-tool — it's how voice profiles like the community-post skill were created.

## Method

### Step 1: Read and Absorb

Read all provided text samples. Don't analyze yet — just absorb. Get a feel for the rhythm, the word choices, the patterns. Read it like a reader, not a critic.

### Step 2: Identify Style Characteristics

Analyze across these dimensions:

- **Tone and voice**: Formal, casual, authoritative, conversational, technical, warm, dry
- **Sentence structure**: Length distribution, complexity, rhythm patterns, use of fragments
- **Word choice and vocabulary**: Technical depth, accessibility, distinctive terms, avoidances
- **Organization and flow**: How ideas connect, paragraph structure, use of transitions
- **Purpose and audience**: Who this is written for, what it aims to achieve
- **Formatting and presentation**: Headers, lists, code blocks, emphasis patterns
- **What's absent**: What this author doesn't do is as revealing as what they do

### Step 3: Extract Representative Passages

Select 5 passages that best exemplify the style. For each, note specifically what makes it characteristic — the sentence structure, the word choice, the way it opens or closes.

### Step 4: Generate Anti-Examples

Write 5 passages that deliberately break the style, each in a different way. For each, explain precisely why it doesn't fit. Common anti-patterns:
- Too formal/academic
- Too casual/slangy
- Too marketing/buzzword-heavy
- Too vague/unspecific
- Too dry/documentation-style (when the author is warmer)
- Too emotional (when the author is restrained)

### Step 5: Synthesize the Guide

Produce a style guide with:

1. **Overall assessment**: 2-3 sentences capturing the essence
2. **Detailed characteristics**: Each with specific examples from the text
3. **Representative passages**: The 5 best examples with annotations
4. **Anti-examples**: The 5 generated violations with explanations
5. **Quick reference rules**: Bullet list of dos and don'ts for someone writing in this voice

## Output Format

The output should be structured as a skill-ready document — someone could take it and use it as a SKILL.md for a new writing voice. Include enough detail that an AI assistant could reliably produce text in this voice without seeing the original samples.

Lay the voice skill out with progressive disclosure:

- `SKILL.md` holds the overall assessment, the detailed characteristics with their examples, and the quick reference rules.
- `references/representative-passages.md` holds the 5 annotated passages. Link it from SKILL.md and say when to read it, for example before drafting a new piece.
- `references/anti-examples.md` holds the 5 anti-examples with explanations. Link it from SKILL.md and say when to read it, for example when checking a draft for drift.
- The frontmatter `description` names the narrow context the voice is for, such as the publication, audience or genre, so the skill does not fire on every writing request.
