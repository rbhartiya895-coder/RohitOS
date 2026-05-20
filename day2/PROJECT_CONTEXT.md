# RohitOS Project Context

## Project Type
Voice-controlled AI assistant built in Python.

---

# Current Features

- Wake word activation
- Continuous listening mode
- Sleep mode
- Text-to-speech
- Speech recognition
- Open websites
- Open apps
- Create folders
- Delete folders

---

# Wake Words

- hey jarvis
- jarvis
- hey rohit
- rohit

---

# Current Commands

- open youtube
- open google
- open chatgpt
- open calculator
- open notepad
- open vs code
- close calculator
- close notepad
- close vs code
- create folder
- delete folder
- time
- who are you
- sleep
- exit

---

# Technologies

- Python 3.12
- speech_recognition
- pyttsx3
- pyaudio

---

# Current Architecture

- Root `main.py` launches the current modular assistant flow
- `core/router.py` classifies commands and routes them to command modules
- `commands/app_commands.py` handles app commands
- `commands/web_commands.py` handles website commands
- `commands/file_commands.py` handles file commands
- `core/memory.py` handles simple persistent memory
- `core/ai_engine.py` handles AI fallback placeholder
- Wake-word/text input work remains part of the assistant foundation

---

# Future Goals

- ChatGPT integration
- AI conversation mode
- Memory system
- GUI interface
- Automation engine
- System controls
- Voice typing
- AI vision

---

# Coding Style

- Beginner-friendly
- Modular functions
- Simple architecture
- Clear comments

---

# Notes

Assistant should behave similar to:
- Jarvis
- Google Assistant
- Alexa

The assistant should:
- stay silent until wake word
- continue listening after activation
- sleep only after stop command

