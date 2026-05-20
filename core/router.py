# core/router.py

from commands import app_commands
from commands import file_commands
from commands import web_commands
from core import memory
from core import ai_engine

def detect_command(command_text):

    command_text = command_text.lower()

    # Web commands
    if "open google" in command_text or "open youtube" in command_text:
        return "web_command"

    # App commands
    elif "open" in command_text:
        return "app_command"

    # Memory commands
    elif "remember" in command_text or "what is my" in command_text:
        return "memory_command"

    # File commands
    elif "create folder" in command_text or "delete folder" in command_text:
        return "file_command"

    # AI fallback
    else:
        return "ai_fallback"


def route_command(command_text):

    command_type = detect_command(command_text)

    # WEB COMMANDS
    if command_type == "web_command":

        site = command_text.replace("open ", "")
        return web_commands.open_website(site)

    # APP COMMANDS
    elif command_type == "app_command":

        app_name = command_text.replace("open ", "")
        return app_commands.open_application(app_name)

    # MEMORY COMMANDS
    elif command_type == "memory_command":

        if "remember" in command_text:

            parts = command_text.split("remember ")[1]

            if " is " in parts:

                key, value = parts.split(" is ", 1)

                return memory.remember(key.strip(), value.strip())

        elif "what is my" in command_text:

            key = command_text.replace("what is my ", "")
            return memory.recall(key.strip())

        return "Memory command not understood."

    # FILE COMMANDS
    elif command_type == "file_command":

        if "create folder" in command_text:

            folder_name = command_text.replace("create folder ", "")
            return file_commands.create_folder(folder_name)

        elif "delete folder" in command_text:

            folder_name = command_text.replace("delete folder ", "")
            return file_commands.delete_folder(folder_name)

        return "File command not understood."

    # AI FALLBACK
    else:
         return ai_engine.ask_ai(command_text)