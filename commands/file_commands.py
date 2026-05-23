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

# INITIALIZE SANDBOX FOLDERS
SANDBOX_FOLDERS = ["downloads", "documents", "images", "test_files"]
for sf in SANDBOX_FOLDERS:
    os.makedirs(os.path.join(WORKSPACE_PATH, sf), exist_ok=True)


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


# -----------------------------------
# ORGANIZE FOLDER
# -----------------------------------

def organize_folder(folder_name):

    target_path = os.path.join(WORKSPACE_PATH, folder_name)

    if not os.path.exists(target_path):
        return f"Folder '{folder_name}' does not exist."

    extensions = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".csv"],
        "Archives": [".zip", ".tar", ".rar", ".7z"],
        "Media": [".mp3", ".mp4", ".wav", ".avi"]
    }

    try:
        files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
        
        if not files:
            return f"Folder '{folder_name}' is empty."

        moved_count = 0
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            category = "Others"

            for cat, exts in extensions.items():
                if ext in exts:
                    category = cat
                    break

            cat_dir = os.path.join(target_path, category)
            os.makedirs(cat_dir, exist_ok=True)

            src = os.path.join(target_path, file)
            dst = os.path.join(cat_dir, file)
            shutil.move(src, dst)
            moved_count += 1

        return f"Organized {moved_count} files in '{folder_name}'."

    except Exception as e:
        print(f"Error organizing folder: {e}")
        return "Error organizing folder."


# -----------------------------------
# SHOW RECENT FILES
# -----------------------------------

def show_recent_files():

    try:
        all_files = []
        for root, dirs, files in os.walk(WORKSPACE_PATH):
            for file in files:
                filepath = os.path.join(root, file)
                all_files.append((filepath, os.path.getmtime(filepath)))

        if not all_files:
            return "No files found in workspace."

        # Sort by modification time descending
        all_files.sort(key=lambda x: x[1], reverse=True)
        recent_files = [os.path.basename(f[0]) for f in all_files[:5]]
        
        return "Recent files: " + ", ".join(recent_files)

    except Exception as e:
        print(f"Error finding recent files: {e}")
        return "Error finding recent files."


# -----------------------------------
# MOVE FILES BY TYPE
# -----------------------------------

def move_files_by_type(file_type):

    file_type = file_type.lower()
    
    if file_type == "pdf":
        target_exts = [".pdf"]
        dest_folder = os.path.join(WORKSPACE_PATH, "documents", "PDFs")
    elif file_type == "image":
        target_exts = [".jpg", ".jpeg", ".png", ".gif"]
        dest_folder = os.path.join(WORKSPACE_PATH, "images")
    else:
        return f"Unknown file type: {file_type}"

    os.makedirs(dest_folder, exist_ok=True)

    sources = ["downloads", "test_files"]
    moved_count = 0

    try:
        for source in sources:
            source_path = os.path.join(WORKSPACE_PATH, source)
            if not os.path.exists(source_path):
                continue
                
            for file in os.listdir(source_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in target_exts:
                    src = os.path.join(source_path, file)
                    if os.path.isfile(src):
                        dst = os.path.join(dest_folder, file)
                        shutil.move(src, dst)
                        moved_count += 1

        return f"Moved {moved_count} {file_type} files."

    except Exception as e:
        print(f"Error moving {file_type} files: {e}")
        return f"Error moving {file_type} files."