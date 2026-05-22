from commands import app_commands
from commands import file_commands
from commands import web_commands

from core import memory
from core import ai_engine

from core.state_manager import (
    set_state,
    SLEEPING,
    SHUTDOWN
)


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
    # SLEEP COMMANDS
    # --------------------------------

    sleep_keywords = [
        "sleep",
        "go to sleep",
        "stop listening"
    ]

    for keyword in sleep_keywords:

        if keyword in command_text:
            return "sleep_command"

    # --------------------------------
    # SHUTDOWN COMMANDS
    # --------------------------------

    shutdown_keywords = [
        "shutdown",
        "shut down",
        "stop",
        "exit",
        "close yourself"
    ]

    for keyword in shutdown_keywords:

        if keyword in command_text:
            return "shutdown_command"

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
# CLEAN MEMORY KEY
# -----------------------------------

def clean_memory_key(key):

    key = key.lower().strip()

    if key.startswith("my "):
        key = key.replace("my ", "", 1)

    return key.strip()


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

                return (
                    "Please say memory like: "
                    "remember name is Rohit"
                )

            key, value = parts.split(
                " is ",
                1
            )

            key = clean_memory_key(key)

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

        key = clean_memory_key(key)

        return memory.recall(key)

    # --------------------------------
    # SHOW MEMORY
    # --------------------------------

    elif command_type == "memory_show":

       return str(memory.show_memory()) 
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
    # SLEEP COMMANDS
    # --------------------------------

    elif command_type == "sleep_command":

        print("RohitOS entering sleep mode...")

        set_state(SLEEPING)

        return "Entering sleep mode."

    # --------------------------------
    # SHUTDOWN COMMANDS
    # --------------------------------

    elif command_type == "shutdown_command":

        print("RohitOS shutting down...")

        set_state(SHUTDOWN)

        return "Shutting down RohitOS."

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:

        return ai_engine.ask_ai(command_text)