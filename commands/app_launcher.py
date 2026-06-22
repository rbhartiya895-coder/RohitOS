import os
import glob

APP_INDEX = {}

def build_app_index():
    global APP_INDEX
    APP_INDEX.clear()
    
    user_start_menu = os.path.expandvars('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs')
    system_start_menu = os.path.expandvars('%ALLUSERSPROFILE%\\Microsoft\\Windows\\Start Menu\\Programs')
    
    for menu in [user_start_menu, system_start_menu]:
        if not os.path.exists(menu):
            continue
        for root, dirs, files in os.walk(menu):
            for file in files:
                if file.endswith('.lnk'):
                    name = os.path.splitext(file)[0].lower()
                    APP_INDEX[name] = os.path.join(root, file)
                    
    # Basic fallbacks if not found in start menu but guaranteed on windows
    if "notepad" not in APP_INDEX:
        APP_INDEX["notepad"] = "notepad.exe"
    if "calculator" not in APP_INDEX:
        APP_INDEX["calculator"] = "calc.exe"

def open_application(app_name):
    app_name = app_name.lower().strip()
    
    # First, direct match
    if app_name in APP_INDEX:
        path = APP_INDEX[app_name]
        os.startfile(path)
        return path
        
    # Second, substring match (e.g., "visual studio code" matches "vscode" or "code")
    for key, path in APP_INDEX.items():
        if app_name in key or key in app_name:
            os.startfile(path)
            return path
            
    return None

# Build index on module import
build_app_index()

