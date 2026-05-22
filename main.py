from dotenv import load_dotenv

load_dotenv()

from voice.listen import listen
from voice.speak import speak

from core.router import route_command

from core.state_manager import (
    get_state,
    is_active,
    is_sleeping,
    is_shutdown,
    set_state,
    ACTIVE
)


print("RohitOS Activated")


# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    # --------------------------------
    # SHUTDOWN CHECK
    # --------------------------------

    if is_shutdown():

        print("RohitOS Fully Shutdown.")

        break

    # --------------------------------
    # ACTIVE MODE
    # --------------------------------

    if is_active():

        command = listen()

        if command:

            response = route_command(command)

            if response:

                print(f"RohitOS: {response}")

                speak(response)

    # --------------------------------
    # SLEEP MODE
    # --------------------------------

    elif is_sleeping():

        print("Waiting for wake word...")

        wake_command = listen()

        if wake_command:

            wake_command = (
                wake_command
                .lower()
                .strip()
            )

            print(
                f"Wake Check: "
                f"{wake_command}"
            )

            # ----------------------------
            # FLEXIBLE WAKE WORDS
            # ----------------------------

            wake_words = [
                "rohit",
                "jarvis",
                "friday",
                "wake up"
            ]

            wake_detected = False

            for wake_word in wake_words:

                if wake_word in wake_command:

                    wake_detected = True

                    break

            # ----------------------------
            # WAKE ACTIVATION
            # ----------------------------

            if wake_detected:

                set_state(ACTIVE)

                print(
                    "RohitOS Activated"
                )

                speak("Yes Boss.")