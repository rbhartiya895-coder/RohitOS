# RohitOS Agent Pipeline

This file explains how to continue RohitOS when one AI tool reaches limits or when multiple assistants are used.

## Current Project Reality

RohitOS is currently a Python voice assistant foundation.

Current implementation:

- Root launcher: `main.py`
- Main assistant code: `day2\assistant.py`
- Project memory docs: `day2\*.md`

Future direction:

- AI OS-style architecture
- modular automation
- memory system
- multi-agent orchestration
- AI routing
- cloud sync
- Telegram control
- PDF and browser automation

Do not treat the future architecture as already built. Build toward it slowly.

## Agent Roles

### Architect: ChatGPT / Claude

Use for:

- daily planning
- concept explanation
- roadmap design
- feature breakdown
- learning support

Do not use for direct file edits unless the full current project context is pasted.

### Chief Engineer: Codex

Use for:

- complex logic review
- security review
- risky file/automation changes
- architecture decisions
- debugging hard failures
- integrating changes safely

Codex should inspect files before editing and update docs after coding.

### Lead Developer: Cline

Use for:

- local VS Code file editing
- boilerplate code
- terminal execution
- simple feature implementation
- directory cleanup
- docs maintenance

Cline should follow `.clinerules`, `AGENTS.md`, and all project docs.

## Cline Configuration

Current Cline setup:

- API provider: Google Gemini
- Model: `gemini-2.5-flash`
- Reasoning mode: balanced / medium-high
- Authentication: Google AI Studio free API key
- Workspace rules: `.clinerules` active

If Cline is used, it must read:

- `.clinerules`
- `AGENTS.md`
- `day2\PROJECT_CONTEXT.md`
- `day2\ROADMAP.md`
- `day2\COMMANDS.md`
- `day2\BUGS.md`
- `day2\DAILY_WORKFLOW.md`

## Required Docs Update Rule

Whenever any agent changes Python code, it must check whether these files need updates:

- `day2\BUGS.md`
- `day2\COMMANDS.md`
- `day2\ROADMAP.md`
- `day2\PROJECT_CONTEXT.md`
- `day2\DAILY_WORKFLOW.md`

Update rules:

- Update `COMMANDS.md` if user commands changed.
- Update `BUGS.md` if a bug was found, fixed, or left unresolved.
- Update `ROADMAP.md` if a milestone changed.
- Update `PROJECT_CONTEXT.md` if behavior or architecture changed.
- Update `DAILY_WORKFLOW.md` only if the workflow changed.

## Safety Rules

- Keep changes small and testable.
- Do not rewrite working code without a clear reason.
- Do not touch banking, OTP, password, payment, or sensitive folders.
- Do not permanently delete user files.
- Risky actions must require confirmation.
- Do not use raw `eval()` or `exec()` for generated code execution.
- Do not run destructive Git commands unless explicitly requested.

## Handoff Prompt For Another Agent

Use this when moving to Cline, Claude, ChatGPT, or terminal Codex:

```text
I am building RohitOS, a Python-based secure personal AI assistant that will grow into an AI OS prototype.

Before coding, read:
- AGENTS.md
- AGENT_PIPELINE.md
- day2\PROJECT_CONTEXT.md
- day2\ROADMAP.md
- day2\COMMANDS.md
- day2\BUGS.md
- day2\DAILY_WORKFLOW.md

Current run command:
py -3.12 main.py

Current assistant file:
day2\assistant.py

Keep changes small and safe. Do not rewrite the whole project. After coding, update project docs if commands, bugs, roadmap, workflow, or architecture changed.
```
