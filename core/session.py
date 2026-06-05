# core/session.py
import os
import json
import re

SESSION_FILE = os.path.join("data", "session.json")

def _ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)

def generate_alias(filename):
    """Generate a friendly alias from a raw filename."""
    name = os.path.splitext(filename)[0].lower()
    # Replace underscores and hyphens with spaces
    name = name.replace("_", " ").replace("-", " ")
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def update_last_file(filepath):
    _ensure_data_dir()
    data = {"aliases": {}}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                if "aliases" not in data:
                    data["aliases"] = {}
        except Exception:
            pass
            
    # Track context
    data["last_opened_file"] = filepath
    
    # Store friendly alias mapping
    filename = os.path.basename(filepath)
    alias = generate_alias(filename)
    
    # Cap alias dict size at 50 to prevent unbounded growth
    if alias not in data["aliases"] and len(data["aliases"]) >= 50:
        first_key = next(iter(data["aliases"]))
        del data["aliases"][first_key]
        
    data["aliases"][alias] = filepath
    
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

def get_document_alias(alias_query):
    """Lookup a filepath by an exact or partial alias match."""
    if not os.path.exists(SESSION_FILE):
        return None, None
        
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            aliases = data.get("aliases", {})
            
            # Exact match
            if alias_query in aliases:
                return aliases[alias_query], alias_query
                
            # Partial match
            for saved_alias, filepath in aliases.items():
                if alias_query in saved_alias:
                    return filepath, saved_alias
                    
            return None, None
    except Exception:
        return None, None
