# commands/app_commands.py
# Handles commands related to opening applications/websites.

def open_application(app_name):
    """Opens the specified application or website."""
    print(f"Opening: {app_name}")
    # In a real scenario, you'd use os.system or subprocess to open applications
    return f"Opened {app_name}"
