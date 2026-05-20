from voice import listen
from voice import speak
from voice import wakeword

from core import router
from core import state_manager

import time


def main():

    print("RohitOS started...")

    while state_manager.assistant_running:

        command = input("You: ").lower()

        # Ignore empty input
        if not command.strip():
            continue

        # EXIT COMMANDS
        if command in wakeword.EXIT_WORDS:

            speak.speak_response("Shutting down RohitOS.")

            state_manager.assistant_running = False

            break

        # WAKE WORDS
        if command in wakeword.WAKE_WORDS:

            state_manager.assistant_active = True

            speak.speak_response("Yes Boss, I am listening.")

            continue

        # SLEEP WORDS
        if command in wakeword.SLEEP_WORDS:

            state_manager.assistant_active = False

            speak.speak_response("Going to sleep.")

            continue

        # IGNORE COMMANDS IF SLEEPING
        if not state_manager.assistant_active:

            print("Assistant sleeping...")

            continue

        # PROCESS COMMAND
        response = router.route_command(command)

        speak.speak_response(response)

        # Small cooldown
        time.sleep(1)


if __name__ == "__main__":
    main()