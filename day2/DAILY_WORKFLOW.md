# RohitOS Daily Workflow

Use this file to keep RohitOS development calm, daily, and practical.

## Roles

### ChatGPT
- Gives the daily learning plan.
- Explains the concept for the day.
- Breaks the idea into small features.
- Helps decide what should be built next.

### Codex
- Edits the real project files.
- Writes and improves Python code.
- Debugs errors from the terminal.
- Tests the code when possible.
- Updates project docs after changes.

## Daily Rule

Build only one main mission per day.

Good daily mission:
- Small enough to finish today.
- Useful for RohitOS.
- Easy to test.
- Connected to the roadmap.

Avoid:
- Adding too many features at once.
- Rewriting working code without a reason.
- Mixing AI, UI, automation, and memory in one day.

## Daily ChatGPT Prompt

Paste this into ChatGPT each day:

```text
I am building RohitOS, a secure personal AI assistant in Python.

Current status:
- Voice wake word works
- Text-to-speech works
- Website/app opening works
- Folder create/open/delete works
- Delete moves folders to RohitOS trash

Give me today's development mission based on this roadmap:
Day 2: Auto file organization
Day 3: Google Drive sync
Day 4: Telegram remote file retrieval
Day 5: PDF reading and summarization
Day 6: Browser automation with Playwright
Day 7: Simple workflow orchestration

Output in this format:
1. Today's goal
2. Why this matters
3. Features to build, maximum 3
4. Commands the assistant should understand
5. Files/modules likely needed
6. Safety rules
7. How to test
8. What I should paste to Codex
```

## Codex Handoff Format

After ChatGPT gives the plan, paste this to Codex:

```text
Today's RohitOS mission:
<paste ChatGPT's plan here>

Please implement this in my project, debug errors, test it, and update docs.
```

## Codex Work Checklist

Codex should do this every coding session:

1. Inspect current files before editing.
2. Make a small plan.
3. Edit only the needed files.
4. Keep risky actions protected by confirmation.
5. Run syntax checks.
6. Tell what changed.
7. Tell exactly how to run and test.

## Current Recommended Next Mission

Day 2: Auto file organization.

Suggested commands:

```text
jarvis organize downloads
jarvis organize documents
jarvis show recent files
jarvis move pdf files
jarvis move image files
```

Safety rules:
- Only organize approved folders.
- Never touch banking, password, payment, or private folders.
- Move files into organized folders, do not permanently delete them.
- Print every moved file path in the terminal.

## End Of Day Notes

At the end of each day, update:

- `COMMANDS.md` with new commands.
- `BUGS.md` with problems found.
- `ROADMAP.md` with completed work.
- `PROJECT_CONTEXT.md` if the architecture changes.
