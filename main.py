import sys
from core import router
from voice import listen, speak
from commands import app_commands, web_commands, file_commands
from core import memory, ai_engine

def main():
    if "--text" not in sys.argv:
        speak.speak_response("RohitOS activated.")

    while True:
        command = listen.listen_for_command()
        if command.lower() in ["exit", "quit"]:
            speak.speak_response("Goodbye!")
            break
        
        # Process command using the router
        response = router.route_command(command)
        speak.speak_response(response)


if __name__ == "__main__":
    main()
