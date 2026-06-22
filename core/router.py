import time
from commands import web_launcher
from commands import web_commands
from commands import search_commands
from commands import file_commands
from commands import app_commands
from commands import study_commands
from commands import system_commands
from core import system_state
from commands import browser_commands
from core import memory
from core import session
from core import ai_engine
from core.intent_understanding import normalize_intent

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
    "facebook",
    "gmail",
    "linkedin"
]

# -----------------------------------
# COMMAND CONSTANTS
# -----------------------------------

IDENTITY_PHRASES = [
    "who are you",
    "what are you"
]

SMALL_TALK_RESPONSES = {
    "hello": "Hello Boss.",
    "hi": "Hi Boss.",
    "hello rohit os": "Hello Boss.",
    "hi rohit os": "Hi Boss.",
    "hello rohitos": "Hello Boss.",
    "hi rohitos": "Hi Boss.",
    "hello rohit": "Hello Boss.",
    "hi rohit": "Hi Boss.",
    "good morning": "Good morning Boss.",
    "good afternoon": "Good afternoon Boss.",
    "good evening": "Good evening Boss.",
    "thank you": "You're welcome Boss.",
    "thanks": "Anytime Boss.",
    "how are you": "I am operating at full capacity.",
    "who made you": "I was created by Rohit."  # DO NOT CHANGE — creator name
}

VALID_STARTS = [
    "what", "how", "why", "who", "when", "where",
    "can", "could", "would", "will", "should",
    "do", "does", "did", "is", "are", "was", "were",
    "tell", "explain", "help", "give", "write", "summarize", "translate", "generate",
    "hello", "hi", "hey", "please"
]

KNOWN_FOLDERS = ["downloads", "documents", "desktop", "pictures"]

FILE_KEYWORDS = ["pdf", "doc", "presentation", "powerpoint", "ppt", "excel", "txt", "notes"]


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
            
    if command_text == "stop":
        return "sleep_command"

    # --------------------------------
    # SHUTDOWN COMMANDS
    # --------------------------------

    shutdown_keywords = [
        "shutdown",
        "shut down",
        "exit rohitos",
        "close rohitos"
    ]

    for keyword in shutdown_keywords:

        if command_text == keyword or command_text.startswith(keyword):
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
        
    if command_text.startswith("forget "):
        return "memory_forget"

    if command_text.startswith("change my ") or command_text.startswith("update my "):
        return "memory_change"
        
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
    
    if command_text.startswith("close "):
        return "close_app"

    # --------------------------------
    # FILE / FOLDER OPENING
    # --------------------------------

    if command_text.startswith("open latest "):
        return "open_latest_file"
        
    if "previous document" in command_text or "document i was reading" in command_text or "pdf i opened earlier" in command_text or "pdf i was reading" in command_text:
        return "open_previous_document"
        
    for folder in KNOWN_FOLDERS:
        if command_text == f"open {folder}":
            return "open_system_folder"
            
    if command_text.startswith("open ") and any(keyword in command_text for keyword in FILE_KEYWORDS):
        return "open_specific_file"
        
    if command_text.startswith("show ") and " notes" in command_text:
        return "open_specific_file"
        
    if command_text.startswith("open "):
        return "open_document_or_app"

    # --------------------------------
    # STUDY COMMANDS
    # --------------------------------
    if command_text == "summarize file":
        return "summarize_file"
    
    if command_text.startswith("create revision notes"):
        return "create_revision_notes"
        
    if command_text == "start study mode":
        return "start_study_mode"

    # --------------------------------
    # GENERIC CONTEXT COMMANDS
    # --------------------------------
    
    if command_text in ["generic_key_points", "generic_summarize", "generic_make_notes"]:
        return command_text

    # --------------------------------
    # BROWSER COMMANDS
    # --------------------------------
    
    if command_text == "get website info":
        return "get_website_info"
    if command_text in ["summarize page", "read summary", "read cached summary"]:
        return "summarize_page"
    if command_text == "get page key points":
        return "get_page_key_points"
    if command_text == "make_page_notes":
        return "make_page_notes"
        
    # --------------------------------
    # EXPLICIT INTENTS (From English layer)
    # --------------------------------
    if command_text in [
        "system_lock", "system_sleep", "system_restart", "system_shutdown",
        "volume_up", "volume_down", "volume_mute", "volume_unmute", "confirm_yes",
        "open_gmail", "open_youtube", "open_chatgpt", "open_github", "open_google",
        "open_downloads", "open_desktop", "open_documents", "open_pictures", "open_videos", "open_music",
        "open_calculator", "open_browser", "open_notepad"
    ]:
        return command_text
    if command_text == "create ppt points":
        return "create_ppt_points"
    if command_text == "save article":
        return "save_article"
    if command_text == "show saved articles":
        return "show_saved_articles"
    if command_text.startswith("confirm delete ") and command_text != "confirm delete folder" and command_text != "confirm delete file":
        return "confirm_delete_saved_article"
        
    if command_text.startswith("delete ") and command_text != "delete file" and command_text != "delete folder":
        if not command_text.startswith("delete file ") and not command_text.startswith("delete folder "):
            return "request_delete_saved_article"

    # --------------------------------
    # SIMPLE INFO COMMANDS
    # --------------------------------

    if command_text in ["time", "what is the time"]:
        return "info_command"
        
    if command_text == "voice_status":
        return "voice_status"
        
    # --------------------------------
    # MATH COMMANDS
    # --------------------------------
    
    math_keywords = ["calculate", "what is", "plus", "minus", "times", "divided by", " x ", " + ", " - ", " / "]
    if any(command_text.startswith(kw) for kw in ["calculate ", "what is "]) or any(char.isdigit() for char in command_text) and any(kw in command_text for kw in math_keywords):
        # Additional check to ensure it's actually math and not just a text with numbers
        if any(op in command_text for op in [" plus ", " minus ", " times ", " divided by ", " x ", "+", "-", "*", "/"]):
            return "math_command"

    # --------------------------------
    # IDENTITY COMMANDS
    # --------------------------------

    if any(phrase in command_text for phrase in IDENTITY_PHRASES):
        return "identity_command"

    # --------------------------------
    # SMALL TALK COMMANDS
    # --------------------------------

    if command_text in SMALL_TALK_RESPONSES:
        return "small_talk_command"

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

    from core.intent_normalizer import normalize
    original_cmd_log = command_text
    command_text = command_text.lower().strip()
    
    # 1. Hindi/Hinglish Intent Normalization Layer
    intent, modified_text = normalize(command_text)
    
    if intent:
        command_type = intent
        command_text = modified_text # standard english format for param extraction
        print(f"Original Command: {original_cmd_log}")
        print(f"Normalized Intent: {command_type}")
    else:
        # 2. Legacy English Intent Understanding
        command_text = normalize_intent(command_text)
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
    # CLOSE APP
    # --------------------------------

    elif command_type == "close_app":

        app_name = command_text.replace(
            "close ",
            ""
        ).strip()

        result = app_commands.close_app(app_name)
        if not result:
            return "Closing application is not yet configured."
        return result
        
    # --------------------------------
    # SYSTEM FOLDERS
    # --------------------------------

    elif command_type == "open_system_folder":
        folder_name = command_text.replace("open ", "").strip()
        return file_commands.open_system_folder(folder_name)
        
    # --------------------------------
    # LATEST/PREVIOUS FILE
    # --------------------------------

    elif command_type == "open_latest_file":
        file_type = command_text.replace("open latest ", "").strip()
        return file_commands.open_latest_file(file_type)

    elif command_type == "open_previous_document":
        return file_commands.open_previous_document()

    # --------------------------------
    # SPECIFIC FILE
    # --------------------------------

    elif command_type == "open_specific_file":
        return file_commands.open_specific_file(command_text.replace("open ", "").strip())
        
    elif command_type == "open_document_or_app":
        target = command_text.replace("open ", "").strip()
        
        # Performance shortcut for known apps to avoid file scan I/O
        standard_apps = ["calculator", "calc", "notepad", "vs code", "vscode", "visual studio code", "code", "chrome", "spotify"]
        if target in standard_apps:
            return app_commands.open_app(target)
            
        print("Document Intelligence Candidate")
        result = file_commands.open_specific_file(target)
        if result == file_commands.FILE_NOT_FOUND_SENTINEL:
            return app_commands.open_app(target)
        return result
        
    # --------------------------------
    # SPECIFIC APP / FILE COMMANDS (Day 19 Normalization)
    # --------------------------------

    elif command_type == "open_calculator":
        return app_commands.open_app("calculator")
        
    elif command_type == "open_browser":
        return app_commands.open_app("chrome")
        
    elif command_type == "open_notepad":
        return app_commands.open_app("notepad")
        
    elif command_type == "open_notes_file":
        target = command_text.replace("open ", "").replace("show ", "").strip()
        return file_commands.open_specific_file(target)

    # --------------------------------
    # DAY 20: FOLDERS & WEBSITES
    # --------------------------------
    elif command_type.startswith("open_") and command_type in [
        "open_downloads", "open_desktop", "open_documents", 
        "open_pictures", "open_videos", "open_music"
    ]:
        folder_name = command_type.split("_")[1]
        return file_commands.open_system_folder(folder_name)
        
    elif command_type.startswith("open_") and command_type in [
        "open_gmail", "open_youtube", "open_chatgpt", 
        "open_github", "open_google"
    ]:
        site_name = command_type.split("_")[1]
        return web_launcher.open_website(site_name)

    # --------------------------------
    # DAY 20: VOLUME & SYSTEM
    # --------------------------------
    elif command_type == "volume_up":
        return system_commands.volume_up()
    elif command_type == "volume_down":
        return system_commands.volume_down()
    elif command_type == "volume_mute":
        return system_commands.mute()
    elif command_type == "volume_unmute":
        return system_commands.unmute()
        
    elif command_type in ["system_shutdown", "system_restart", "system_sleep"]:
        system_state.set_pending_system_action(command_type)
        return "Are you sure?"
        
    elif command_type == "confirm_yes":
        pending = system_state.get_pending_system_action()
        if not pending:
            return "Pending action expired or not found."
            
        system_state.clear_pending_system_action()
        
        if pending == "system_shutdown":
            return system_commands.shutdown_computer()
        elif pending == "system_restart":
            return system_commands.restart_computer()
        elif pending == "system_sleep":
            return system_commands.sleep_computer()
            
    elif command_type == "system_lock":
        return system_commands.lock_computer()

    # --------------------------------
    # STUDY COMMANDS
    # --------------------------------

    elif command_type == "summarize_file":
        return study_commands.summarize_file()
        
    elif command_type == "create_revision_notes":
        custom_name = None
        if " called " in command_text:
            custom_name = command_text.split(" called ", 1)[1].strip()
        elif " named " in command_text:
            custom_name = command_text.split(" named ", 1)[1].strip()
        return study_commands.create_revision_notes(custom_name)
        
    elif command_type == "start_study_mode":
        return study_commands.start_study_mode()
    # --------------------------------
    # GENERIC CONTEXT COMMANDS
    # --------------------------------
    
    elif command_type in ["generic_key_points", "generic_summarize", "generic_make_notes"]:
        active = session.get_active_context_type()
        if active == "browser":
            # Treat as browser command
            ok = browser_commands.get_current_page()
            if not ok and not session.get_browser_context():
                return "Please summarize a webpage first."
                
            if command_type == "generic_key_points":
                return browser_commands.get_key_points()
            elif command_type == "generic_summarize":
                return browser_commands.summarize_page()
            elif command_type == "generic_make_notes":
                return browser_commands.make_notes()
        else:
            # Treat as document command
            if command_type == "generic_key_points":
                return study_commands.get_key_points()
            elif command_type == "generic_summarize":
                return study_commands.summarize_file()
            elif command_type == "generic_make_notes":
                return study_commands.create_revision_notes()

    # --------------------------------
    # BROWSER COMMANDS
    # --------------------------------
    
    elif command_type in ["get_website_info", "summarize_page", "get_page_key_points", "make_page_notes", "create_ppt_points", "save_article"]:
        # Update browser context before doing any browser commands
        ok = browser_commands.get_current_page()
        if not ok and not session.get_browser_context():
            return "No browser page detected. Please open a webpage first."
        
        if command_type == "get_website_info":
            return browser_commands.get_website_info()
        elif command_type == "summarize_page":
            return browser_commands.summarize_page()
        elif command_type == "get_page_key_points":
            return browser_commands.get_key_points()
        elif command_type == "make_page_notes":
            return browser_commands.make_notes()
        elif command_type == "create_ppt_points":
            return browser_commands.create_ppt_points()
        elif command_type == "save_article":
            return browser_commands.save_article()

    elif command_type == "show_saved_articles":
        return browser_commands.show_saved_articles()
            
    elif command_type == "request_delete_saved_article":
        target = command_text.replace("delete ", "").strip()
        return f"Are you sure you want to delete '{target}'? Say 'confirm delete {target}' to proceed."
        
    elif command_type == "confirm_delete_saved_article":
        target = command_text.replace("confirm delete ", "").strip()
        return browser_commands.delete_saved_article(target)

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
                return memory.remember_fact(parts.strip())

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
    # MEMORY FORGET
    # --------------------------------

    elif command_type == "memory_forget":

        key = command_text.replace("forget my ", "").replace("forget ", "").strip()
        key = clean_memory_key(key)
        
        return memory.forget(key)

    # --------------------------------
    # MEMORY CHANGE / UPDATE
    # --------------------------------

    elif command_type == "memory_change":

        prefix = "change my " if command_text.startswith("change my ") else "update my "

        if " to " in command_text:
            parts = command_text.replace(prefix, "").split(" to ", 1)
            
            if len(parts) == 2:
                key, value = parts
                key = clean_memory_key(key)
                return memory.remember(key.strip(), value.strip())
                
        return f"Please say it like: {prefix}branch to AI"

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
    # MATH COMMANDS
    # --------------------------------

    elif command_type == "math_command":
        import re
        import ast
        import operator as op
        
        expr = command_text.replace("calculate ", "").replace("what is ", "").strip()
        expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*").replace(" x ", " * ").replace("divided by", "/")
        expr = expr.replace(" and ", " + ") # "calculate X and Y" usually means add
        
        # Keep only math characters
        safe_expr = re.sub(r'[^0-9\+\-\*\/\.\(\) ]', '', expr)
        
        _ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}
        def _safe_eval(node):
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.BinOp):
                return _ops[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
            raise ValueError("Unsupported expression")
            
        try:
            # Safe evaluation without eval()
            result = _safe_eval(ast.parse(safe_expr, mode='eval').body)
            # Format nicely
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return f"The answer is {result}."
        except Exception:
            return "I couldn't calculate that."

    # --------------------------------
    # SIMPLE INFO COMMANDS
    # --------------------------------

    elif command_type == "info_command":

        current_time = time.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    elif command_type == "voice_status":
        import core.voice_router as voice_router
        return voice_router.get_voice_status()

    # --------------------------------
    # IDENTITY COMMANDS
    # --------------------------------

    elif command_type == "identity_command":

        return "I am RohitOS, your personal AI assistant."

    # --------------------------------
    # SMALL TALK COMMANDS
    # --------------------------------

    elif command_type == "small_talk_command":

        return SMALL_TALK_RESPONSES.get(command_text, "Yes Boss.")

    # --------------------------------
    # AI FALLBACK
    # --------------------------------

    else:

        if len(command_text) < 3 or not is_genuine_request(command_text):
            return "I did not understand that command."

        return ai_engine.ask_ai(command_text)