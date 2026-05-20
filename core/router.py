# core/router.py

from commands import app_commands
from commands import file_commands
from commands import web_commands

from core import memory
from core import ai_engine


# -----------------------------------
# DETECT COMMAND TYPE
# -----------------------------------

def detect_command(command_text):

    command_text = command_text.lower()

    websites = [
        "google",
        "youtube",
        "github",
        "chatgpt",
        "chat gpt",
        "instagram",
        "facebook"
    ]

    # --------------------------------
    # CLOSE APP COMMANDS
    # --------------------------------

    if "close" in command_text:
        return "close_app"

    # --------------------------------
    # WEB COMMANDS
    # --------------------------------

    for site in websites:

        if f"open {site}" in command_text:
            return "web_command"

    # --------------------------------
    # APP COMMANDS
    # --------------------------------

    if "open" in command_text:
        return "app_command"

    # --------------------------------
    # MEMORY COMMANDS
    # --------------------------------

    elif "remember" in command_text:
        return "memory_command"

    elif "what is my" in command_text:
        return "memory_command"

    # --------------------------------
    # FILE COMMANDS
    # --------------------------------

    elif "create folder" in command_text:
        return "file_command"

    elif "delete folder" in command_text:
        return "file_command"

    # --------------------------------
    # STOP / SLEEP COMMANDS
    # --------------------------------

    elif "stop" in command_text:
        return "stop_command"

    elif "go to sleep" in command_text:
        return "stop_command"

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:
        return "ai_fallback"


# -----------------------------------
# ROUTE COMMAND
# -----------------------------------

def route_command(command_text):

    command_type = detect_command(command_text)

    print(f"Command Received: {command_text}")
    print(f"Detected Type: {command_type}")

    # --------------------------------
    # WEB COMMANDS
    # --------------------------------

    if command_type == "web_command":

        site = command_text.replace("open ", "").strip()

        return web_commands.open_website(site)

    # --------------------------------
    # APP COMMANDS
    # --------------------------------

    elif command_type == "app_command":

        app_name = command_text.replace("open ", "").strip()

        return app_commands.open_app(app_name)

    # --------------------------------
    # CLOSE APP COMMANDS
    # --------------------------------

    elif command_type == "close_app":

        app_name = command_text.replace("close ", "").strip()

        return app_commands.close_app(app_name)

    # --------------------------------
    # MEMORY COMMANDS
    # --------------------------------

    elif command_type == "memory_command":

        # REMEMBER SOMETHING
        if "remember" in command_text:

            try:

                parts = command_text.split("remember ")[1]

                if " is " in parts:

                    key, value = parts.split(" is ", 1)

                    return memory.remember(
                        key.strip(),
                        value.strip()
                    )

            except:

                return "Could not save memory."

        # RECALL MEMORY
        elif "what is my" in command_text:

            key = command_text.replace(
                "what is my ",
                ""
            ).strip()

            return memory.recall(key)

        return "Memory command not understood."

    # --------------------------------
    # FILE COMMANDS
    # --------------------------------

    elif command_type == "file_command":

        # CREATE FOLDER
        if "create folder" in command_text:

            folder_name = command_text.replace(
                "create folder ",
                ""
            ).strip()

            return file_commands.create_folder(folder_name)

        # DELETE FOLDER
        elif "delete folder" in command_text:

            folder_name = command_text.replace(
                "delete folder ",
                ""
            ).strip()

            return file_commands.delete_folder(folder_name)

        return "File command not understood."

    # --------------------------------
    # STOP COMMAND
    # --------------------------------

    elif command_type == "stop_command":

        print("RohitOS entering sleep mode...")

        exit()

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:

        return ai_engine.ask_ai(command_text)