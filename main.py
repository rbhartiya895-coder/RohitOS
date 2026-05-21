from dotenv import load_dotenv

load_dotenv()

from voice.listen import listen
from voice.speak import speak

from core.router import route_command
from core.state_manager import assistant_running


print("RohitOS Activated")


while assistant_running:

    command = listen()

    if command:

        response = route_command(command)

        # PRINT RESPONSE
        if response:

            print(f"RohitOS: {response}")

            # SPEAK RESPONSE
            speak(response)