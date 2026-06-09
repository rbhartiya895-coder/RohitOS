# test_sarvam_tts.py
import sys
import os

# Ensure the root directory is in sys.path so we can import modules properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from voice.sarvam_tts import speak

if __name__ == "__main__":
    try:
        print("Testing Sarvam TTS directly...")
        speak("Hello Boss. Rahul voice is now active.")
        print("Test passed successfully.")
    except Exception as e:
        print(f"Test failed with error: {e}")
