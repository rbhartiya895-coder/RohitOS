# voice/speak.py
# Handles text-to-speech output

import pyttsx3


import sys
import subprocess

def speak(text):
    try:
        print(f"RohitOS says: {text}")
        print("[TTS Speaking]")

        # Isolate SAPI5 in a completely independent subprocess
        # This completely bypasses the PyAudio / COM message loop starvation on real machines
        # Use stdin to pass text to avoid backslash/character injection errors
        script = 'import sys, pyttsx3\ntext = sys.stdin.read()\nengine = pyttsx3.init()\nengine.setProperty("rate", 170)\nengine.say(text)\nengine.runAndWait()'
        
        subprocess.run([sys.executable, "-c", script], input=text, text=True, encoding='utf-8', check=True)
        print("[TTS Completed]")

    except Exception as e:
        print(f"[TTS Error] {e}")