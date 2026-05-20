import os


def open_application(app_name):

    app_name = app_name.lower().strip()

    if app_name == "calculator":
        os.system("calc")
        return "Opened calculator"

    elif app_name == "notepad":
        os.system("notepad")
        return "Opened notepad"

    return "Application not found"