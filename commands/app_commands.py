# commands/app_commands.py

import subprocess
import os
import shutil

# -----------------------------------
# HELPER: FIND START MENU SHORTCUT
# -----------------------------------
def _find_start_menu_shortcut(app_name):
    start_menu_paths = [
        os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
    ]
    
    app_name_clean = app_name.lower().replace(" ", "")
    
    for path in start_menu_paths:
        if not os.path.exists(path):
            continue
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    if app_name_clean in file.lower().replace(" ", ""):
                        return os.path.join(root, file)
    return None

# -----------------------------------
# OPEN APPLICATIONS
# -----------------------------------

def open_app(app_name):

    app_name = app_name.lower().strip()

    # CALCULATOR
    if "calculator" in app_name or app_name == "calc":
        subprocess.Popen("calc")
        return "Opening Calculator"

    # NOTEPAD
    elif "notepad" in app_name:
        subprocess.Popen("notepad")
        return "Opening Notepad"
        
    # DYNAMIC APP DISCOVERY
    
    # 1. Try shutil.which
    executable = shutil.which(app_name)
    if executable:
        subprocess.Popen(executable)
        return f"Opening {app_name}"
        
    # 2. Try common aliases
    if "vscode" in app_name or "code" in app_name:
        if shutil.which("code"):
            subprocess.Popen("code")
            return "Opening VS Code"
            
    # 3. Try start menu shortcuts
    shortcut = _find_start_menu_shortcut(app_name)
    if shortcut:
        os.startfile(shortcut)
        return f"Opening {app_name}"

    # 4. Fallback cmd start
    try:
        subprocess.Popen(["cmd", "/c", "start", "", app_name])
        return f"Attempting to open {app_name}"
    except Exception:
        return "Application not recognized or installed."


# -----------------------------------
# CLOSE APPLICATIONS
# -----------------------------------

def close_app(app_name):

    app_name = app_name.lower()

    # CLOSE NOTEPAD
    if "notepad" in app_name:

        os.system("taskkill /f /im notepad.exe")

        msg = "Closing Notepad"
        print(msg)
        return msg

    # CLOSE CALCULATOR
    elif "calculator" in app_name:

        os.system("taskkill /f /im CalculatorApp.exe")

        msg = "Closing Calculator"
        print(msg)
        return msg

    else:

        msg = "Application not recognized"
        print(msg)
        return msg