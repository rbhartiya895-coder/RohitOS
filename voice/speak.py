# voice/speak.py
# Handles text-to-speech output

import pyttsx3


# -----------------------------------
# GLOBAL TTS ENGINE
# -----------------------------------

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    print("TTS Status: Engine Initialized")
except Exception as e:
    engine = None
    print(f"TTS Status: Engine Initialization Failed ({e})")


# -----------------------------------
# SPEAK FUNCTION
# -----------------------------------

def speak(text):
    global engine
    try:
        print(f"RohitOS says: {text}")

        if engine:
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        else:
            print("TTS Status: Speech Degraded (Engine unavailable)")

    except Exception as e:
        print(f"Speech Error: {e}")
        # Re-initialize engine to recover from bad state
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
        except Exception:
            engine = None