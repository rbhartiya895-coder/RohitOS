from commands import app_commands
from commands import file_commands
from commands import web_commands

from core import memory
from core import ai_engine


# -----------------------------------
# WEBSITE LIST
# -----------------------------------

WEBSITES = [
    "google",
    "youtube",
    "github",
    "chatgpt",
    "chat gpt",
    "instagram",
    "facebook"
]


# -----------------------------------
# DETECT COMMAND TYPE
# -----------------------------------

def detect_command(command_text):

    command_text = command_text.lower().strip()

    # --------------------------------
    # STOP / SLEEP COMMANDS
    # --------------------------------

    stop_commands = [
        "stop",
        "stop listening",
        "sleep",
        "go to sleep",
        "exit",
        "shutdown"
    ]

    if command_text in stop_commands:
        return "stop_command"

    # --------------------------------
    # MEMORY COMMANDS
    # --------------------------------

    if command_text.startswith("remember "):
        return "memory_save"

    if command_text.startswith("what is my "):
        return "memory_recall"

    if command_text == "show memory":
        return "memory_show"

    # --------------------------------
    # FILE COMMANDS
    # --------------------------------

    if command_text.startswith("create folder "):
        return "create_folder"

    if command_text.startswith("delete folder "):
        return "delete_folder"

    # --------------------------------
    # WEBSITE COMMANDS
    # --------------------------------

    for site in WEBSITES:

        if command_text == f"open {site}":
            return "web_command"

    # --------------------------------
    # APP COMMANDS
    # --------------------------------

    if command_text.startswith("open "):
        return "open_app"

    if command_text.startswith("close "):
        return "close_app"

    # --------------------------------
    # SIMPLE INFO COMMANDS
    # --------------------------------

    if command_text == "time":
        return "info_command"

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    return "ai_fallback"


# -----------------------------------
# ROUTE COMMAND
# -----------------------------------

def route_command(command_text):

    command_text = command_text.lower().strip()

    command_type = detect_command(command_text)

    print(f"Command Received: {command_text}")
    print(f"Detected Type: {command_type}")

    # --------------------------------
    # WEBSITE COMMANDS
    # --------------------------------

    if command_type == "web_command":

        site = command_text.replace(
            "open ",
            ""
        ).strip()

        return web_commands.open_website(site)

    # --------------------------------
    # OPEN APP
    # --------------------------------

    elif command_type == "open_app":

        app_name = command_text.replace(
            "open ",
            ""
        ).strip()

        return app_commands.open_app(app_name)

    # --------------------------------
    # CLOSE APP
    # --------------------------------

    elif command_type == "close_app":

        app_name = command_text.replace(
            "close ",
            ""
        ).strip()

        return app_commands.close_app(app_name)

    # --------------------------------
    # MEMORY SAVE
    # --------------------------------

    elif command_type == "memory_save":

        try:

            parts = command_text.split(
                "remember ",
                1
            )[1]

            if " is " not in parts:
                return "Please say memory like: remember name is Rohit"

            key, value = parts.split(
                " is ",
                1
            )

            return memory.remember(
                key.strip(),
                value.strip()
            )

        except Exception as e:

            print(f"Memory Save Error: {e}")

            return "Could not save memory."

    # --------------------------------
    # MEMORY RECALL
    # --------------------------------

    elif command_type == "memory_recall":

        key = command_text.replace(
            "what is my ",
            ""
        ).strip()

        return memory.recall(key)

    # --------------------------------
    # SHOW MEMORY
    # --------------------------------

    elif command_type == "memory_show":

        return memory.show_memory()

    # --------------------------------
    # CREATE FOLDER
    # --------------------------------

    elif command_type == "create_folder":

        folder_name = command_text.replace(
            "create folder ",
            ""
        ).strip()

        return file_commands.create_folder(folder_name)

    # --------------------------------
    # DELETE FOLDER
    # --------------------------------

    elif command_type == "delete_folder":

        folder_name = command_text.replace(
            "delete folder ",
            ""
        ).strip()

        return file_commands.delete_folder(folder_name)

    # --------------------------------
    # STOP COMMANDS
    # --------------------------------

    elif command_type == "stop_command":

        print("RohitOS entering sleep mode...")

        exit()

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:

        return ai_engine.ask_ai(command_text)