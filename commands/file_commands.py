# commands/file_commands.py

import os
import shutil
import stat
from core import session


# -----------------------------------
# WORKSPACE PATH
# -----------------------------------

WORKSPACE_PATH = "rohitos_workspace"

# -----------------------------------
# FILE EXTENSIONS
# -----------------------------------
FILE_EXTENSIONS = {
    "pdf": ".pdf",
    "presentation": ".pptx",
    "powerpoint": ".pptx",
    "ppt": ".pptx",
    "doc": ".docx",
    "word": ".docx",
    "excel": ".xlsx",
    "text": ".txt",
    "notes": ".txt",
    "image": [".jpg", ".png", ".jpeg"],
    "picture": [".jpg", ".png", ".jpeg"]
}

# -----------------------------------
# GET APPROVED FOLDERS
# -----------------------------------
def _get_approved_folders():
    user_profile = os.environ.get("USERPROFILE", "")
    return [
        os.path.join(user_profile, "Documents"),
        os.path.join(user_profile, "Downloads"),
        os.path.join(user_profile, "Desktop"),
        WORKSPACE_PATH
    ]

# -----------------------------------
# SYSTEM FOLDER CONTROL
# -----------------------------------
def open_system_folder(folder_name):
    user_profile = os.environ.get("USERPROFILE", "")
    folder_map = {
        "downloads": os.path.join(user_profile, "Downloads"),
        "documents": os.path.join(user_profile, "Documents"),
        "desktop": os.path.join(user_profile, "Desktop"),
        "pictures": os.path.join(user_profile, "Pictures")
    }
    
    path = folder_map.get(folder_name)
    if path and os.path.exists(path):
        os.startfile(path)
        return f"Opening {folder_name} folder."
        
    return f"Could not find {folder_name} folder."

# -----------------------------------
# OPEN SPECIFIC FILE
# -----------------------------------
def open_specific_file(command_text):
    
    target_ext = None
    target_keyword = command_text
    
    for key, ext in FILE_EXTENSIONS.items():
        if key in command_text:
            target_ext = ext
            target_keyword = command_text.replace(key, "").strip()
            break
            
    if not target_keyword:
        return "Please specify a file name."
        
    # Search approved folders
    matches = []
    for folder in _get_approved_folders():
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            depth = root.replace(folder, "").count(os.sep)
            if depth > 2:
                dirs.clear()  # stop descending
                continue
            for file in files:
                if target_keyword in file.lower():
                    if target_ext is None or file.lower().endswith(target_ext):
                        matches.append(os.path.join(root, file))
                        
    if matches:
        # Open most recently modified match
        matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        os.startfile(matches[0])
        session.update_last_file(matches[0])
        return f"Opening {os.path.basename(matches[0])}."
        
    return f"Could not find a file matching '{target_keyword}'."

# -----------------------------------
# OPEN LATEST FILE
# -----------------------------------
def open_latest_file(file_type):
    
    target_ext = FILE_EXTENSIONS.get(file_type)
    if not target_ext:
        # Fallback to literal extension
        target_ext = "." + file_type
        
    matches = []
    for folder in _get_approved_folders():
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            depth = root.replace(folder, "").count(os.sep)
            if depth > 2:
                dirs.clear()  # stop descending
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if isinstance(target_ext, list):
                    if ext in target_ext:
                        matches.append(os.path.join(root, file))
                else:
                    if ext == target_ext:
                        matches.append(os.path.join(root, file))
                        
    if matches:
        matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        os.startfile(matches[0])
        session.update_last_file(matches[0])
        return f"Opening latest {file_type}."
        
    return f"No recent {file_type} files found."


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

    sources = SANDBOX_FOLDERS
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