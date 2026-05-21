# voice/speak.py
# Handles text-to-speech output

import pyttsx3


# -----------------------------------
# SPEAK FUNCTION
# -----------------------------------

def speak(text):

    try:

        print(f"RohitOS says: {text}")

        # CREATE NEW ENGINE EACH TIME
        engine = pyttsx3.init()

        engine.setProperty("rate", 170)

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print(f"Speech Error: {e}")