# core/router.py
# Central routing system for RohitOS.

def detect_command(command_text):
    """Detects the type of command and routes it accordingly."""
    # Placeholder for actual command detection and routing logic
    if "open" in command_text:
        return "app_command"
    elif "remember" in command_text or "what is my" in command_text:
        return "memory_command"
    elif "create folder" in command_text or "delete folder" in command_text or "open folder" in command_text or "list folder" in command_text:
        return "file_command"
    else:
        return "ai_fallback"

def route_command(command_text):
    from commands import app_commands, file_commands, web_commands
    from core import memory, ai_engine

    command_type = detect_command(command_text)

    if command_type == "app_command":
        if "youtube" in command_text:
            return web_commands.open_website("https://www.youtube.com")
        elif "vscode" in command_text:
            return app_commands.open_application("Visual Studio Code")
        else:
            app_name = command_text.replace("open ", "")
            return app_commands.open_application(app_name)
    elif command_type == "memory_command":
        if "remember" in command_text:
            parts = command_text.split("remember ", 1)[1].split(" is ", 1)
            if len(parts) == 2:
                key, value = parts[0], parts[1]
                return memory.remember(key, value)
            else:
                return "Sorry, I didn't understand what you want me to remember."
        elif "what is my" in command_text:
            key = command_text.replace("what is my ", "").strip("?")
            value = memory.recall(key)
            if value:
                return f"Your {key} is {value}"
            else:
                return f"I don't remember your {key}."
    elif command_type == "file_command":
        if "create folder" in command_text:
            folder_name = command_text.replace("create folder ", "")
            return file_commands.create_folder(folder_name)
        # Add more file commands here later
    else:
        return ai_engine.ask_ai(command_text)
