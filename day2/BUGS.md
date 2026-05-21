# RohitOS Known Bugs

---

# HIGH PRIORITY

## Gemini Quota Exhaustion
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

## Sleep Command Exits Assistant Fully
STATUS: ACTIVE

Problem:
- The 'sleep' command currently terminates the assistant process entirely.
- Expected behavior is to enter a low-power, inactive state until reactivated.

Possible Fixes:
- Implement a proper sleep/wake-word reactivation loop.
- Ensure background listening for wake words while in sleep mode.

---

## Speech Recognition Mistakes
STATUS: ACTIVE

Problem:
- Speech recognition frequently misinterprets commands or words.
- Affects accuracy and user experience.

Possible Fixes:
- Microphone tuning.
- Porcupine wake-word engine.
- Whisper integration.
- Noise filtering.
- Improved language models.

---

## Multi-Command Parsing Not Implemented
STATUS: ACTIVE

Problem:
- The system can only process one command at a time.
- Cannot handle complex requests with multiple actions.

Possible Fixes:
- Implement a command chaining or multi-intent parsing system.
- Use AI to break down complex requests into sub-commands.

---

## Deprecated Gemini Package Warning
STATUS: ACTIVE

Problem:
- The current Gemini package is deprecated, leading to warnings.
- May cause future compatibility issues.

Possible Fixes:
- Update to the latest supported Gemini package or alternative.
- Refactor code to align with new API standards.

---

# MEDIUM PRIORITY

## Wake Word Reliability
STATUS: ACTIVE

Problem:
- Wake word sometimes misses voice.
- Indian accent detection inconsistent.

Possible Fixes:
- Microphone tuning.
- Porcupine wake-word engine.
- Whisper integration.
- Noise filtering.

---

## Speech Recognition Delay
STATUS: ACTIVE

Problem:
- Delays before command detection.

Possible Fixes:
- Optimize timeout values.
- Async listening.
- Faster recognition engine.

---

## Background Noise Issues
STATUS: ACTIVE

Problem:
- Fan sounds and room noise affect detection.

Possible Fixes:
- Noise suppression.
- Better microphone calibration.
- Offline speech models.

---

## CPU Usage
STATUS: ACTIVE

Problem:
- Continuous listening consumes CPU.

Possible Fixes:
- Threading.
- Async architecture.
- Optimized loops.

---

## Internet Dependency
STATUS: ACTIVE

Problem:
- Speech recognition depends on online APIs.

Possible Fixes:
- Whisper.
- Vosk.
- Offline speech recognition.

---

# LOW PRIORITY

## Browser Control Limitations
STATUS: ACTIVE

Problem:
- Browser tab closing not fully implemented.

Future Fix:
- Browser automation layer.
- Playwright integration.

---

## Limited Application Detection
STATUS: ACTIVE

Problem:
- Some installed apps are not detected.

Possible Fix:
- App registry scanning.
- Shortcut indexing.

---

## Missing Permission Layer
STATUS: ACTIVE

Problem:
- No security confirmation system yet.

Future Fix:
- Confirmation prompts.
- Permission manager.
- Safe automation mode.

---

# CURRENT ENGINEERING FOCUS

Current priority is:
1. Stability
2. Routing
3. Memory
4. AI interaction
5. Offline capability

NOT adding advanced automation yet.