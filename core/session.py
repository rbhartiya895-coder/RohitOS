# core/session.py
import os
import json

SESSION_FILE = os.path.join("data", "session.json")

def _ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)

def update_last_file(filepath):
    _ensure_data_dir()
    data = {}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            pass
            
    data["last_opened_file"] = filepath
    
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving session: {e}")

def get_last_file():
    if not os.path.exists(SESSION_FILE):
        return None
        
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_opened_file")
    except Exception:
        return None
