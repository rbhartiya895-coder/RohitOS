# core/voice_router.py
# Central router for voice operations, managing modes and fallbacks.

import os
from dotenv import load_dotenv

load_dotenv()

# We import the legacy speech system and the new Sarvam TTS / Whisper STT systems
from voice.speak import speak as legacy_speak
from voice.sarvam_tts import speak as sarvam_speak

from voice.listen import listen as legacy_listen
from voice.whisper_stt import listen as whisper_listen
from voice.whisper_stt import get_whisper_model_info

# Options: "sarvam", "legacy"
VOICE_MODE = "sarvam"

# Options: "whisper", "legacy"
STT_MODE = "legacy"

def speak(text):
    global VOICE_MODE
    
    if VOICE_MODE == "sarvam":
        try:
            sarvam_speak(text)
            return
        except Exception as e:
            print(f"[Sarvam TTS Failed] {e}")
            print("Switching to Legacy TTS")
            # Automatically fallback to legacy
            legacy_speak(text)
    else:
        legacy_speak(text)

def listen(timeout=5):
    global STT_MODE
    
    if STT_MODE == "whisper":
        try:
            return whisper_listen(timeout=timeout)
        except Exception as e:
            print(f"[Whisper Failed] {e}")
            print("Switching to Legacy STT")
            STT_MODE = "legacy"
            return legacy_listen(timeout=timeout)
    else:
        return legacy_listen(timeout=timeout)

def get_voice_status():
    whisper_model = get_whisper_model_info() if STT_MODE == "whisper" else "N/A"
    return (f"Current STT is {STT_MODE.capitalize()}. "
            f"Whisper Model is {whisper_model}. "
            f"Current TTS is {VOICE_MODE.capitalize()}.")
