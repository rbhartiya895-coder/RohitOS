from voice.listen import listen
from core.router import route_command
from core.state_manager import assistant_running


print("RohitOS Activated")


while assistant_running:

    command = listen()

    if command:

        route_command(command)