# core/startup_manager.py
# Handles one-time startup initialization

from datetime import datetime


def get_greeting():

    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning Boss. RohitOS online."
    elif 12 <= hour < 17:
        return "Good afternoon Boss. RohitOS online."
    elif 17 <= hour < 22:
        return "Good evening Boss. RohitOS online."
    else:
        return "RohitOS online. Ready when you are."


def run_startup(speak_fn):

    print("=" * 40)
    print(" RohitOS Activated ")
    print("=" * 40)

    greeting = get_greeting()

    print(f"System: {greeting}")
    speak_fn(greeting)
