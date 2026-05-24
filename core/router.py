import time
from commands import app_commands
from commands import file_commands
from commands import web_commands
from commands import search_commands
from core import memory
from core import ai_engine

from core.runtime_states import (
    set_state,
    SLEEPING,
    STOPPED
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
# COMMAND CONSTANTS
# -----------------------------------

IDENTITY_PHRASES = [
    "who are you",
    "what are you"
]

VALID_STARTS = [
    "what", "how", "why", "who", "when", "where",
    "can", "could", "would", "will", "should",
    "do", "does", "did", "is", "are", "was", "were",
    "tell", "explain", "help", "give", "write", "summarize", "translate", "generate",
    "hello", "hi", "hey", "please"
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
    # SEARCH COMMANDS
    # --------------------------------

    if (
        command_text.startswith("search ")
        and " on google" in command_text
    ):
        return "google_search"

    if (
        command_text.startswith("search ")
        and " on youtube" in command_text
    ):
        return "youtube_search"
    # --------------------------------
    # FILE COMMANDS
    # --------------------------------

    if command_text.startswith("create folder "):
        return "create_folder"

    if command_text.startswith("delete folder "):
        return "delete_folder"

    if command_text.startswith("create file "):
        return "create_file"

    if command_text.startswith("delete file "):
        return "delete_file"

    # --------------------------------
    # FILE ORGANIZATION COMMANDS
    # --------------------------------

    if command_text.startswith("organize "):
        return "organize_folder"

    if command_text == "show recent files":
        return "show_recent_files"

    if command_text.startswith("move ") and command_text.endswith(" files"):
        return "move_files"

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

    if command_text in ["time", "what is the time"]:
        return "info_command"

    # --------------------------------
    # IDENTITY COMMANDS
    # --------------------------------

    if any(phrase in command_text for phrase in IDENTITY_PHRASES):
        return "identity_command"

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    return "ai_fallback"


# -----------------------------------
# HELPER: VALIDATE GENUINE REQUEST
# -----------------------------------

def is_genuine_request(command_text):

    for start in VALID_STARTS:
        if command_text.startswith(start):
            return True

    return False


# -----------------------------------
# CLEAN MEMORY KEY
# -----------------------------------

def clean_memory_key(key):

    key = key.lower().strip()

    if key.startswith("my "):
        key = key.replace("my ", "", 1)

    return key.strip()


# -----------------------------------
# STRIP FILLERS
# -----------------------------------

def strip_fillers(name):

    fillers = ["the ", "a ", "an "]
    for filler in fillers:
        if name.startswith(filler):
            return name[len(filler):].strip()
    return name


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
    # GOOGLE SEARCH
    # --------------------------------

    elif command_type == "google_search":

        query = command_text.replace(
            "search ",
            ""
        ).replace(
            " on google",
            ""
        ).strip()

        if not query:
            return "Please tell me what to search for, like 'search cat on google'."

        return search_commands.search_google(query)

    # --------------------------------
    # YOUTUBE SEARCH
    # --------------------------------

    elif command_type == "youtube_search":

        query = command_text.replace(
            "search ",
            ""
        ).replace(
            " on youtube",
            ""
        ).strip()

        if not query:
            return "Please tell me what to search for, like 'search cat on youtube'."

        return search_commands.search_youtube(query)
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
        
        folder_name = strip_fillers(folder_name)

        return file_commands.create_folder(folder_name)

    # --------------------------------
    # DELETE FOLDER
    # --------------------------------

    elif command_type == "delete_folder":

        folder_name = command_text.replace(
            "delete folder ",
            ""
        ).strip()
        
        folder_name = strip_fillers(folder_name)

        return file_commands.delete_folder(folder_name)

    # --------------------------------
    # CREATE FILE
    # --------------------------------

    elif command_type == "create_file":

        file_name = command_text.replace(
            "create file ",
            ""
        ).strip()
        
        file_name = strip_fillers(file_name)

        return file_commands.create_file(file_name)

    # --------------------------------
    # DELETE FILE
    # --------------------------------

    elif command_type == "delete_file":

        file_name = command_text.replace(
            "delete file ",
            ""
        ).strip()
        
        file_name = strip_fillers(file_name)

        return file_commands.delete_file(file_name)

    # --------------------------------
    # FILE ORGANIZATION COMMANDS
    # --------------------------------

    elif command_type == "organize_folder":

        folder_name = command_text.replace(
            "organize ",
            ""
        ).strip()
        
        folder_name = strip_fillers(folder_name)

        return file_commands.organize_folder(folder_name)

    elif command_type == "show_recent_files":

        return file_commands.show_recent_files()

    elif command_type == "move_files":

        file_type = command_text.replace(
            "move ",
            ""
        ).replace(
            " files",
            ""
        ).strip()

        return file_commands.move_files_by_type(file_type)

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

        set_state(STOPPED)

        return "Shutting down RohitOS."

    # --------------------------------
    # SIMPLE INFO COMMANDS
    # --------------------------------

    elif command_type == "info_command":

        current_time = time.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # --------------------------------
    # IDENTITY COMMANDS
    # --------------------------------

    elif command_type == "identity_command":

        return "I am RohitOS, your personal AI assistant."

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:

        if len(command_text) < 3 or not is_genuine_request(command_text):
            return "I did not understand that command."

        return ai_engine.ask_ai(command_text)