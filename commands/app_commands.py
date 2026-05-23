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

        msg = "Opening Calculator"
        print(msg)
        return msg

    # NOTEPAD
    elif "notepad" in app_name:

        subprocess.Popen("notepad")

        msg = "Opening Notepad"
        print(msg)
        return msg

    else:

        msg = "Application not recognized"
        print(msg)
        return msg


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