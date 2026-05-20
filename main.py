from voice import listen
from voice import speak
from core import router


def main():

    command = input("You: ")

    response = router.route_command(command)

    speak.speak_response(response)


if __name__ == "__main__":
    main()