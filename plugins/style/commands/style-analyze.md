---
description: Analyze writing samples to produce a style guide that could become a voice skill
argument-hint: <file_path_or_glob>
---

# Style Analyze

Analyze writing samples and produce a comprehensive style guide.

## Process

1. **Load the style-analysis skill** and follow its method.

2. **Read the samples** at `$ARGUMENTS`. This can be:
   - A single file path
   - Multiple files (read each one)
   - A glob pattern's worth of files

3. **Follow the five-step analysis method** from the skill:
   - Read and absorb (don't analyze yet)
   - Identify style characteristics across all dimensions
   - Extract 5 representative passages with annotations
   - Generate 5 anti-examples with explanations
   - Synthesize into a complete style guide

4. **Output the style guide** in a format ready to become a SKILL.md for a new voice. The output should be detailed enough that an AI assistant could reliably write in this voice without seeing the original samples.

5. **Show the result** to the user. If they want to save it as a skill, they can tell you where.
