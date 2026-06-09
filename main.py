import sys
import time
from dotenv import load_dotenv

load_dotenv()

from core.voice_router import listen, speak
from core.router import route_command
from core.startup_manager import run_startup
from core.runtime_states import (
    is_active,
    is_sleeping,
    is_processing,
    is_stopped,
    set_state,
    ACTIVE,
    PROCESSING
)

# -----------------------------------
# STARTUP INITIALIZATION
# -----------------------------------

if "--startup-delay" in sys.argv:
    print("Waiting 3 seconds for audio drivers to initialize...")
    time.sleep(3)

run_startup(speak)

# -----------------------------------
# WAKE WORDS
# -----------------------------------

WAKE_WORDS = [
    "rohit",
    "jarvis",
    "friday",
    "wake up"
]

# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:
    try:
        if is_stopped():
            print("RohitOS Fully Shutdown.")
            break

        if is_processing():
            # Prevents microphone polling while handling a command
            time.sleep(0.1)
            continue

        if is_active():

            command = listen(timeout=5)

            if command:
                set_state(PROCESSING)
                
                response = route_command(command)

                if response:
                    print(f"RohitOS: {response}")
                    speak(response)

                # Revert to ACTIVE only if router didn't transition to SLEEP/STOP
                if is_processing():
                    set_state(ACTIVE)

        elif is_sleeping():

            print("Waiting for wake word...")
            wake_command = listen(timeout=3)

            if wake_command:
                wake_command = wake_command.lower().strip()
                print(f"Wake Check: {wake_command}")

                wake_detected = any(w in wake_command for w in WAKE_WORDS)

                if wake_detected:
                    set_state(ACTIVE)
                    print("RohitOS Activated")
                    speak("Yes Boss.")
                else:
                    # Sleep cooldown on incorrect word
                    time.sleep(1.5)
            else:
                # Sleep cooldown on silence
                time.sleep(1.5)
                
    except Exception as e:
        print(f"\n[Main Loop Error] Unexpected failure: {e}")
        try:
            speak("Recovering from an unexpected error.")
        except Exception:
            pass
            
        time.sleep(2)
        # Attempt to reset state safely to prevent deadlock
        if is_processing():
            set_state(ACTIVE)
        continue