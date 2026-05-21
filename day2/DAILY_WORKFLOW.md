# RohitOS Daily Workflow

Purpose:
Keep RohitOS development organized, stable, and realistic.

---

# DEVELOPMENT PRINCIPLES

## Core Rule
Build ONE meaningful feature at a time.

Avoid:
- giant rewrites
- random feature additions
- AI-generated chaos
- mixing multiple systems together

---

# DAILY WORKFLOW

## Step 1 — Review Context
Before coding:
- read PROJECT_CONTEXT.md
- read ROADMAP.md
- read BUGS.md
- check previous session notes

---

## Step 2 — Decide Daily Mission
A good mission is:
- small enough to finish
- easy to test
- useful for the assistant
- connected to roadmap goals

Examples:
- improve router
- add memory persistence
- improve speech handling

---

## Step 3 — Architecture First
Before coding:
- decide affected modules
- avoid unnecessary rewrites
- keep changes isolated

Rule:
Think first. Generate later.

---

## Step 4 — Build In Small Parts

Recommended process:

1. plan
2. build one file
3. test
4. debug
5. continue

Never build huge systems in one step.

---

# AI WORKFLOW

## ChatGPT Role
Use ChatGPT for:
- architecture
- planning
- debugging help
- code explanation
- modular code generation
- roadmap guidance

NOT for:
- blindly generating giant systems

---

## Local AI Role
Use local AI tools for:
- small edits
- syntax fixes
- boilerplate
- comments
- refactoring help

Recommended:
- Ollama
- Continue.dev
- DeepSeek Coder
- Qwen Coder

---

# CODING RULES

## File Rules
- Keep files small.
- One responsibility per file.
- Use readable names.
- Avoid giant functions.

---

## Safety Rules
- Never auto-delete important files.
- Require confirmation for risky actions.
- Keep backup/rollback possible.

---

## Testing Rules
After every feature:
- run manually
- test edge cases
- confirm voice still works
- confirm router still works

---

# DOCUMENTATION RULES

At the end of EVERY coding session update:

## ROADMAP.md
Update:
- completed work
- next targets
- feature status

---

## BUGS.md
Update:
- new bugs
- bug fixes
- priorities

---

## COMMANDS.md
Update:
- new commands
- removed commands
- changed command syntax

---

## PROJECT_CONTEXT.md
Update ONLY if:
- architecture changes
- major systems added
- folder structure changes

---

# SESSION LOG FORMAT

Create:

```plaintext
SESSION_LOGS/