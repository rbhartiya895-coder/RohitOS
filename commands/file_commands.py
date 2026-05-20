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

        print(f"Folder '{folder_name}' created successfully")

    except Exception as e:

        print("Error creating folder:", e)


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

            print(f"Folder '{folder_name}' deleted successfully")

        else:

            print("Folder does not exist")

    except Exception as e:

        print("Error deleting folder:", e)
        