# commands/file_commands.py

import os
import shutil
import stat
import difflib
import PyPDF2
from collections import Counter
import re
from core import session


# -----------------------------------
# WORKSPACE PATH
# -----------------------------------

WORKSPACE_PATH = "rohitos_workspace"
FILE_NOT_FOUND_SENTINEL = "__FILE_NOT_FOUND__"

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

STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of", "is", "are", "was", "were", "be", "been", "this", "that", "it", "from", "as", "not", "no", "we", "you", "they", "i", "he", "she"}

def _extract_pdf_keywords(filepath):
    try:
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # Read first page only for extremely fast context extraction
            if reader.pages:
                text = reader.pages[0].extract_text() or ""
        
        # Clean text
        words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        words = [w for w in words if w not in STOP_WORDS]
        
        # Get top 5 most common long words
        counts = Counter(words)
        return [word for word, count in counts.most_common(5)]
    except Exception:
        return []

def _track_and_open_file(filepath):
    os.startfile(filepath)
    session.update_last_file(filepath)
    
    if filepath.lower().endswith(".pdf"):
        keywords = _extract_pdf_keywords(filepath)
        if keywords:
            session.store_document_keywords(filepath, keywords)
            print(f"Extracted Keywords: {keywords}")

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

def open_previous_document():
    last_file = session.get_last_file()
    if last_file and os.path.exists(last_file):
        _track_and_open_file(last_file)
        return f"Opening {os.path.basename(last_file)}."
    return "No recent document found."

# -----------------------------------
# OPEN SPECIFIC FILE
# -----------------------------------
def open_specific_file(command_text):
    
    # 0. Check Revision Notes Override First
    if command_text in ["revision notes", "revision note"]:
        last_note = session.get_last_revision_note()
        if last_note and os.path.exists(last_note):
            _track_and_open_file(last_note)
            return f"Opening {os.path.basename(last_note)}."

    target_ext = None
    target_keyword = command_text
    
    for key, ext in FILE_EXTENSIONS.items():
        if key in command_text:
            target_ext = ext
            target_keyword = command_text.replace(key, "").strip()
            break
            
    if not target_keyword:
        return "Please specify a file name."
        
    # 1. Check Session Aliases First (Fuzzy)
    alias_path, matched_alias, match_type = session.get_document_alias(target_keyword)
    if alias_path and os.path.exists(alias_path):
        _track_and_open_file(alias_path)
        if match_type == "alias":
            print(f"Matched Alias: {matched_alias}")
        elif match_type == "keyword":
            print(f"Matched Keywords: {matched_alias}")
        return f"Opening {os.path.basename(alias_path)}."

    # 3. Search approved folders (Fuzzy Filename)
    all_files = []
    for folder in _get_approved_folders():
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            depth = root.replace(folder, "").count(os.sep)
            if depth > 2:
                dirs.clear()
                continue
            for file in files:
                file_lower = file.lower()
                if target_ext is None or file_lower.endswith(target_ext) or (isinstance(target_ext, list) and os.path.splitext(file_lower)[1] in target_ext):
                    all_files.append(os.path.join(root, file))
                        
    if all_files:
        filenames_no_ext = [os.path.splitext(os.path.basename(f))[0].lower() for f in all_files]
        
        # 1. Strict Match
        strict_matches = difflib.get_close_matches(target_keyword, filenames_no_ext, n=1, cutoff=0.7)
        if strict_matches:
            best_name = strict_matches[0]
            best_match = next(f for f, n in zip(all_files, filenames_no_ext) if n == best_name)
            _track_and_open_file(best_match)
            print(f"Matched Filename: {strict_matches[0]}")
            return f"Opening {os.path.basename(best_match)}."
            
        # 2. Substring Match
        substring_matches = []
        for f in all_files:
            file_lower = os.path.basename(f).lower()
            if target_keyword in file_lower or target_keyword.replace(" ", "_") in file_lower:
                substring_matches.append(f)
                
        if len(substring_matches) == 1:
            _track_and_open_file(substring_matches[0])
            print(f"Matched Filename: {os.path.basename(substring_matches[0])}")
            return f"Opening {os.path.basename(substring_matches[0])}."
        elif len(substring_matches) > 1:
            names = [os.path.basename(sm) for sm in substring_matches[:3]]
            if len(names) == 2:
                return f"Did you mean {names[0]} or {names[1]}?"
            else:
                return f"Did you mean {', '.join(names[:-1])}, or {names[-1]}?"
            
        # 3. Low Confidence Match (Suggestions)
        low_conf_matches = difflib.get_close_matches(target_keyword, filenames_no_ext, n=3, cutoff=0.3)
        if low_conf_matches:
            names = []
            for best_name in low_conf_matches:
                best_match = next(f for f, n in zip(all_files, filenames_no_ext) if n == best_name)
                names.append(os.path.basename(best_match))
                
            if len(names) == 1:
                return f"Did you mean {names[0]}?"
            elif len(names) == 2:
                return f"Did you mean {names[0]} or {names[1]}?"
            else:
                return f"Did you mean {', '.join(names[:-1])}, or {names[-1]}?"
        
    return FILE_NOT_FOUND_SENTINEL

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
        _track_and_open_file(matches[0])
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