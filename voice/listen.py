# voice/listen.py
# Handles voice listening and recognition.

import sys

def listen_for_command():
    """Listens for a voice command and returns the transcribed text."""
    # Placeholder for actual voice recognition
    if "--text" in sys.argv:
        return input("Enter command (text mode): ")  # For text mode testing
    else:
        return "voice command detected" # Placeholder for actual voice input
