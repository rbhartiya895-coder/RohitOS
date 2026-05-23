# commands/file_commands.py

import os
import shutil
import stat


# -----------------------------------
# WORKSPACE PATH
# -----------------------------------

WORKSPACE_PATH = "rohitos_workspace"


# CREATE WORKSPACE IF NOT EXISTS
if not os.path.exists(WORKSPACE_PATH):

    os.makedirs(WORKSPACE_PATH)


# -----------------------------------
# CREATE FOLDER
# -----------------------------------

def create_folder(folder_name):

    try:

        folder_path = os.path.join(
            WORKSPACE_PATH,
            folder_name
        )

        os.makedirs(folder_path, exist_ok=True)

        msg = f"Folder '{folder_name}' created successfully"
        print(msg)
        return msg

    except Exception as e:

        msg = f"Error creating folder: {e}"
        print(msg)
        return msg


# -----------------------------------
# FORCE DELETE HANDLER
# -----------------------------------

def remove_readonly(func, path, excinfo):

    os.chmod(path, stat.S_IWRITE)

    func(path)


# -----------------------------------
# DELETE FOLDER
# -----------------------------------

def delete_folder(folder_name):

    try:

        folder_path = os.path.join(
            WORKSPACE_PATH,
            folder_name
        )

        if os.path.exists(folder_path):

            shutil.rmtree(
                folder_path,
                onerror=remove_readonly
            )

            msg = f"Folder '{folder_name}' deleted successfully"
            print(msg)
            return msg

        else:

            msg = "Folder does not exist"
            print(msg)
            return msg

    except Exception as e:

        print("Error deleting folder:", e)
        return "Error deleting folder"


# -----------------------------------
# CREATE FILE
# -----------------------------------

def create_file(file_name):

    if "." not in file_name:
        file_name += ".txt"

    try:

        file_path = os.path.join(
            WORKSPACE_PATH,
            file_name
        )

        with open(file_path, "w") as f:
            pass

        msg = f"File '{file_name}' created successfully"
        print(msg)
        return msg

    except Exception as e:

        msg = f"Error creating file: {e}"
        print(msg)
        return msg


# -----------------------------------
# DELETE FILE
# -----------------------------------

def delete_file(file_name):

    try:

        file_path = os.path.join(
            WORKSPACE_PATH,
            file_name
        )

        if os.path.exists(file_path):

            os.remove(file_path)

            msg = f"File '{file_name}' deleted successfully"
            print(msg)
            return msg

        else:

            msg = "File does not exist"
            print(msg)
            return msg

    except Exception as e:

        msg = f"Error deleting file: {e}"
        print(msg)
        return msg