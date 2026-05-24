# PROJECT_CONTEXT.md

````md
# RohitOS Project Context

## Project Vision
RohitOS is a modular AI assistant and future AI operating system prototype built in Python.

Goal:
Build a stable, voice-controlled personal AI assistant that can:
- understand commands
- manage workflows
- automate desktop tasks
- remember context
- assist with productivity
- eventually evolve into a Jarvis-style AI system

---

# Current Development Philosophy

Current focus is NOT advanced agents.

Priority order:
1. Stability
2. Clean architecture
3. Reliable voice interaction
4. Memory and routing
5. Automation later

The assistant must remain:
- beginner-friendly
- modular
- debuggable
- easy to scale later

---

# Current Working Features

## Voice System
- Speech recognition
- Text-to-speech
- Wake-word activation
- Sleep mode
- Continuous listening loop

## Commands
- Open websites
- Open desktop apps
- Create folders
- Delete folders
- Basic memory commands
- Time/info commands
- File organization (sandbox)

## Architecture
- Router-based modular assistant
- Command separation system
- Persistent memory foundation
- AI fallback placeholder

---

# Current Architecture

Assistant Flow:

User Input
    ↓
Wake Word Detection
    ↓
Router
    ↓
Command Module
    ↓
Execution
    ↓
Voice/Text Response

---

# Current Folder Structure

```plaintext
RohitOS/
│
├── core/
│   ├── router.py
│   ├── memory.py
│   ├── ai_engine.py
│   ├── voice.py
│   └── config.py
│
├── commands/
│   ├── app_commands.py
│   ├── web_commands.py
│   ├── file_commands.py
│   └── search_commands.py
│
├── data/
│   └── logs/
│
├── docs/
│   ├── ROADMAP.md
│   ├── BUGS.md
│   ├── COMMANDS.md
│   ├── PROJECT_CONTEXT.md
│   └── DAILY_WORKFLOW.md
│
└── main.py

Note: `rohitos_workspace/` and `data/memory.json` are excluded via `.gitignore` to protect runtime data.
````

---

# Current Technologies

## Core Stack

* Python 3.12
* speech_recognition
* pyttsx3
* pyaudio

## Planned Stack

* Whisper
* Ollama
* ChromaDB
* SQLite
* Playwright

---

# Current Development Phase

## PHASE 1 — FOUNDATION STABILITY

Current mission:

* improve routing
* improve memory
* improve AI interaction
* improve stability
* reduce bugs

NOT focusing on:

* multi-agent systems
* autonomous AI
* complex GUI
* cloud infrastructure

---

# Design Rules

## Architecture Rules

* Keep modules small.
* Keep files readable.
* One responsibility per file.
* Avoid giant AI-generated files.
* Test every feature separately.

## Safety Rules

* Dangerous commands require confirmation.
* Never permanently delete files automatically.
* Avoid uncontrolled automation.
* Keep manual override possible.

---

# Current Status

## Stable

* basic voice assistant loop
* command routing
* app opening
* website opening
* folder operations
* sleep mode

## In Progress

* AI conversation
* memory improvement
* smarter routing
* offline speech support

## Experimental

* local AI
* automation workflows
* browser automation

---

# Long-Term Vision

RohitOS should eventually become:

* personal AI operating system
* workflow automation engine
* research assistant
* desktop productivity AI
* voice-controlled computer interface

Future advanced goals:

* AI vision
* contextual memory
* plugin system
* voice authentication
* multi-step workflows
* AI planning system

````

---

# ROADMAP.md

```md
# RohitOS Development Roadmap

---

# PHASE 1 — FOUNDATION

Goal:
Build a stable assistant core before advanced AI features.

---

## ✅ COMPLETED

### Day 1 — Setup
STATUS: STABLE

Completed:
- Python setup
- VS Code setup
- Package installation
- Project initialization

---

### Day 2 — Voice Assistant Core
STATUS: STABLE

Completed:
- Wake-word system
- Speech recognition
- Text-to-speech
- Continuous listening
- Sleep mode
- Open websites
- Open apps
- Create folders
- Delete folders

---

### Day 3 — Modular Architecture
STATUS: STABLE

Completed:
- Router system
- Command modules
- Basic memory system
- AI fallback structure
- Modular file separation

---

### Day 4–5 — Stability Improvements
STATUS: IN PROGRESS

Completed:
- Improved routing
- Better command checks
- Safer browser handling
- Improved project structure

Still improving:
- wake-word reliability
- listening stability
- AI response system
- memory handling

---

### Day 8 — Runtime Infrastructure
STATUS: STABLE

Completed:
- Centralized Runtime States
- Sleep vs Stop Separation
- Lower CPU Wake Listener
- Windows Startup Activation
- Startup Greeting

---

# 🚧 CURRENT TARGET — DAY 9

STATUS: ACTIVE

Main Goal:
Wait for the next module.

---

# PHASE 2 — REAL ASSISTANT EXPERIENCE

STATUS: FUTURE

Features:
- contextual conversations
- personality system
- offline AI support
- Whisper speech recognition
- improved TTS
- async listening
- command chaining

---

# PHASE 3 — AUTOMATION SYSTEM

STATUS: FUTURE

Features:
- browser automation
- workflow engine
- file organization
- screenshot system
- reminder engine
- automation pipelines

---

# PHASE 4 — ADVANCED AI OS

STATUS: FUTURE

Features:
- local LLM integration
- autonomous agents
- AI vision
- plugin marketplace
- multi-agent workflows
- smart desktop management

---

# LONG-TERM GOAL

Build RohitOS into:
- personal AI assistant
- AI productivity OS
- voice-controlled desktop system
- research assistant
- automation engine
- startup-grade AI prototype
````

---

# BUGS.md

```md
# RohitOS Known Bugs

---

# HIGH PRIORITY

## AI Quota Exhaustion
STATUS: ACTIVE

Problem:
- External AI services hit usage limits quickly.
- Development slows due to API restrictions.

Temporary Solution:
- Use ChatGPT for planning.
- Keep code modular.
- Build manually in smaller steps.

Future Fix:
- Ollama local models
- OpenRouter fallback
- Better AI workflow separation

---

## Wake Word Reliability
STATUS: ACTIVE

Problem:
- Wake word sometimes misses voice.
- Indian accent detection inconsistent.

Possible Fixes:
- microphone tuning
- Porcupine wake-word engine
- Whisper integration
- noise filtering

---

## Speech Recognition Delay
STATUS: ACTIVE

Problem:
- Delays before command detection.

Possible Fixes:
- optimize timeout values
- async listening
- faster recognition engine

---

# MEDIUM PRIORITY

## Background Noise Issues
STATUS: ACTIVE

Problem:
- Fan sounds and room noise affect detection.

Possible Fixes:
- noise suppression
- better microphone calibration
- offline speech models

---

## CPU Usage
STATUS: ACTIVE

Problem:
- Continuous listening consumes CPU.

Possible Fixes:
- threading
- async architecture
- optimized loops

---

## Internet Dependency
STATUS: ACTIVE

Problem:
- Speech recognition depends on online APIs.

Possible Fixes:
- Whisper
- Vosk
- offline speech recognition

---

# LOW PRIORITY

## Browser Control Limitations
STATUS: ACTIVE

Problem:
- Browser tab closing not fully implemented.

Future Fix:
- browser automation layer
- Playwright integration

---

## Limited Application Detection
STATUS: ACTIVE

Problem:
- Some installed apps are not detected.

Possible Fix:
- app registry scanning
- shortcut indexing

---

## Missing Permission Layer
STATUS: ACTIVE

Problem:
- No security confirmation system yet.

Future Fix:
- confirmation prompts
- permission manager
- safe automation mode

---

# CURRENT ENGINEERING FOCUS

Current priority is:
1. stability
2. routing
3. memory
4. AI interaction
5. offline capability

NOT adding advanced automation yet.
```

---

# COMMANDS.md

```md
# RohitOS Commands

---

# Wake Words

Supported:
- hey jarvis
- jarvis
- hey rohit
- rohit

Future:
- custom wake words
- offline wake-word engine
- hotkey activation

---

# CURRENT COMMANDS

## Greetings
STATUS: STABLE

Commands:
- hello
- hi
- good morning
- good evening

---

## Websites
STATUS: STABLE

Commands:
- open youtube
- open google
- open chatgpt
- open github

---

## Applications
STATUS: STABLE

Commands:
- open calculator
- open notepad
- open vs code
- close calculator
- close notepad
- close vs code

---

## Folder Management
STATUS: STABLE

Commands:
- create folder <name>
- delete folder <name>

Examples:
- create folder movies
- delete folder movies

---

## Information Commands
STATUS: STABLE

Commands:
- time
- who are you
- your name

---

## Memory Commands
STATUS: IN PROGRESS

Commands:
- remember <key> is <value>
- what is my <key>
- show memory

---

## Assistant Control
STATUS: STABLE

Commands:
- sleep
- go to sleep
- stop listening
- shutdown
- exit

---

# PLANNED COMMANDS

## File Management
STATUS: FUTURE

Planned:
- create file
- delete file
- rename file
- move file
- organize downloads

---

## System Controls
STATUS: FUTURE

Planned:
- shutdown pc
- restart pc
- volume up
- volume down
- brightness control

---

## AI Commands
STATUS: FUTURE

Planned:
- answer questions
- summarize text
- explain concepts
- internet search
- AI conversations

---

## Automation Commands
STATUS: FUTURE

Planned:
- browser automation
- workflow execution
- screenshot capture
- smart desktop control
```

---

# DAILY_WORKFLOW.md

````md
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
````

Each day:

```plaintext
day_6.md
```

Store:

* what built
* what fixed
* bugs found
* next targets
* stable working state

---

# CURRENT DEVELOPMENT PRIORITY

## PHASE 1 — FOUNDATION

Current focus:

* stability
* routing
* memory
* AI interaction
* voice improvements

---

## PHASE 2 — ASSISTANT EXPERIENCE

Later focus:

* contextual conversations
* personality
* offline AI
* better speech systems

---

## PHASE 3 — AUTOMATION

Only after stability:

* workflows
* browser automation
* desktop control
* smart actions

---

# IMPORTANT MINDSET

RohitOS should become:

* stable first
* smart second
* autonomous later

Do NOT chase complexity too early.

```
```
