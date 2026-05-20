# RohitOS Known Bugs & Improvements

---

# Current Known Issues

## Wake Word Sensitivity
- Sometimes requires loud voice
- Sometimes misses Indian accent pronunciation
- Wake words like "Rohit" are less reliable

Possible Fixes:
- Better microphone tuning
- Offline wake-word model
- Porcupine AI wake-word engine

---

## Speech Recognition Delay
- Assistant occasionally pauses before detecting command

Possible Fixes:
- Optimize timeout values
- Faster recognition engine

---

## Background Noise
- Fan sounds or room noise can affect recognition

Possible Fixes:
- Noise filtering
- Better microphone calibration

---

## CPU Usage
- Continuous listening loop uses CPU constantly

Possible Fixes:
- Threading
- Async architecture
- Optimized listener engine

---

## Internet Dependency
- Speech recognition depends on Google API

Possible Fixes:
- Offline speech recognition
- Whisper integration

---

# Future Improvements

## Voice Improvements
- Natural voice
- Female/male voice selection
- Voice cloning

---

## AI Improvements
- ChatGPT integration
- Memory system
- Context awareness

---

## UI Improvements
- Jarvis animation
- Voice waveform
- Floating assistant window

---

# Notes

Current assistant architecture is:
- beginner-friendly
- modular
- stable for small projects

Needs scaling improvements later for:
- multitasking
- threading
- AI memory
- real-time processing