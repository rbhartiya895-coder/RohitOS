# RohitOS Codex Guidelines

RohitOS is a Python-based secure personal AI assistant / AI OS prototype.

## Project Context

- Main project folder: `C:\Users\Rishabh Bhartiya\OneDrive\Documents\RohitOS`
- Entry point: `main.py`
- Current assistant implementation: `day2\assistant.py`
- Python version: Python 3.12
- Main run command: `py -3.12 main.py`

Before coding, read these files:

- `AGENT_PIPELINE.md`
- `docs\PROJECT_CONTEXT.md`
- `docs\ROADMAP.md`
- `docs\COMMANDS.md`
- `docs\BUGS.md`
- `docs\DAILY_WORKFLOW.md`

## Working Rules

- Build one main mission per day.
- Keep changes small, useful, and testable.
- Prefer simple Python code for deterministic tasks.
- Use AI only for reasoning, summarization, planning, or semantic understanding.
- Do not overbuild with complex frameworks until the project actually needs them.
- Keep RohitOS beginner-friendly while slowly improving architecture.

## Safety Rules

- Never access banking apps, OTP messages, password managers, payment apps, or sensitive folders.
- Risky actions must require human confirmation.
- Folder delete must not permanently delete files; move items to RohitOS trash/logs instead.
- Do not modify `.vscode`, `.sixth`, credentials, environment files, or system settings unless explicitly requested.
- Do not use raw `eval()` or `exec()` for generated code.
- Do not run destructive commands like `git reset --hard`, recursive delete, or broad cleanup unless explicitly requested.

## Coding Rules

- Inspect current files before editing.
- Prefer editing `day2\assistant.py` for current assistant behavior.
- Keep `main.py` as a small launcher unless there is a clear reason to change it.
- Gradually move code into modules later:
  - `voice\listener.py`
  - `voice\speaker.py`
  - `brain\command_router.py`
  - `automation\apps.py`
  - `automation\files.py`
  - `memory\database.py`
- Use clear function names and simple comments.
- Avoid duplicate backup files in the project root; use Git or documented backups instead.

## Testing Rules

After Python changes, run at least:

```powershell
py -3.12 -m py_compile main.py
py -3.12 -m py_compile day2\assistant.py
```

When possible, test in text mode before voice mode:

```powershell
py -3.12 main.py --text
```

Then test voice mode:

```powershell
py -3.12 main.py
```

## Documentation Rules

After coding, update project memory:

- Update `docs\COMMANDS.md` when commands change.
- Update `docs\BUGS.md` when bugs are found or fixed.
- Update `docs\ROADMAP.md` when a milestone is completed.
- Update `docs\PROJECT_CONTEXT.md` when architecture or current behavior changes.
- Update `docs\DAILY_WORKFLOW.md` only when the workflow itself changes.

## Current Roadmap

Completed:

- Day 1: setup and first voice assistant
- Day 2: wake words, voice commands, app open/close, folder create/open/safe-delete, VS Code command, project cleanup

Recommended next mission:

- Day 3: Auto file organization

Suggested Day 3 commands:

- `jarvis organize downloads`
- `jarvis organize documents`
- `jarvis show recent files`
- `jarvis move pdf files`
- `jarvis move image files`
