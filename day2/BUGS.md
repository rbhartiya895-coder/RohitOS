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