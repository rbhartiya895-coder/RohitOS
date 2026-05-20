# commands/app_commands.py

import subprocess
import os


# -----------------------------------
# OPEN APPLICATIONS
# -----------------------------------

def open_app(app_name):

    app_name = app_name.lower()

    # CALCULATOR
    if "calculator" in app_name:

        subprocess.Popen("calc")

        print("Opening Calculator")

    # NOTEPAD
    elif "notepad" in app_name:

        subprocess.Popen("notepad")

        print("Opening Notepad")

    else:

        print("Application not recognized")


# -----------------------------------
# CLOSE APPLICATIONS
# -----------------------------------

def close_app(app_name):

    app_name = app_name.lower()

    # CLOSE NOTEPAD
    if "notepad" in app_name:

        os.system("taskkill /f /im notepad.exe")

        print("Closing Notepad")

    # CLOSE CALCULATOR
    elif "calculator" in app_name:

        os.system("taskkill /f /im CalculatorApp.exe")

        print("Closing Calculator")

    else:

        print("Application not recognized")