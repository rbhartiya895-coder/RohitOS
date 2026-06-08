# core/session.py
import os
import json
import re

SESSION_FILE = os.path.join("data", "session.json")

def _ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)

import difflib

def generate_aliases(filename):
    """Generate friendly aliases from a raw filename."""
    base_alias = os.path.splitext(filename)[0].lower()
    base_alias = base_alias.replace("_", " ").replace("-", " ")
    base_alias = re.sub(r'\s+', ' ', base_alias).strip()
    
    aliases = [base_alias]
    lower_name = filename.lower()
    if "aadhaar" in lower_name:
        aliases.extend(["id proof", "identity document", "aadhaar card"])
    elif "resume" in lower_name or "cv" in lower_name:
        aliases.extend(["resume", "cv", "curriculum vitae"])
    elif "investor" in lower_name or "demo" in lower_name:
        aliases.extend(["investor presentation", "investor pitch", "demo presentation"])
    elif "assignment" in lower_name:
        aliases.extend(["assignment", "homework"])
    elif "os" in lower_name and "notes" in lower_name:
        aliases.extend(["os notes", "operating system notes"])
        
    return list(set(aliases))

def _update_session_key(key, value):
    _ensure_data_dir()
    data = {"aliases": {}, "document_keywords": {}}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                if "aliases" not in data:
                    data["aliases"] = {}
                if "document_keywords" not in data:
                    data["document_keywords"] = {}
        except Exception:
            pass
            
    data[key] = value
    
    if key == "last_opened_file":
        filename = os.path.basename(value)
        aliases = generate_aliases(filename)
        for alias in aliases:
            if alias not in data["aliases"] and len(data["aliases"]) >= 100:
                first_key = next(iter(data["aliases"]))
                del data["aliases"][first_key]
            data["aliases"][alias] = value
        
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving session: {e}")

def update_last_file(filepath):
    _update_session_key("last_opened_file", filepath)

def store_document_keywords(filepath, keywords):
    _ensure_data_dir()
    data = {"aliases": {}, "document_keywords": {}}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                if "document_keywords" not in data:
                    data["document_keywords"] = {}
        except Exception:
            pass
            
    data["document_keywords"][filepath] = keywords
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def get_last_file():
    if not os.path.exists(SESSION_FILE):
        return None
        
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_opened_file")
    except Exception:
        return None

def update_last_revision_note(filepath):
    _update_session_key("last_revision_note", filepath)

def get_last_revision_note():
    if not os.path.exists(SESSION_FILE):
        return None
        
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_revision_note")
    except Exception:
        return None

def get_document_alias(alias_query):
    """Lookup a filepath by an exact, fuzzy, or keyword match."""
    if not os.path.exists(SESSION_FILE):
        return None, None
        
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            aliases = data.get("aliases", {})
            document_keywords = data.get("document_keywords", {})
            
            alias_query_lower = alias_query.lower()
            
            # Exact match
            if alias_query_lower in aliases:
                return aliases[alias_query_lower], alias_query_lower
                
            # Fuzzy match aliases
            matches = difflib.get_close_matches(alias_query_lower, aliases.keys(), n=1, cutoff=0.6)
            if matches:
                return aliases[matches[0]], matches[0]
                
            # Keyword match
            if len(alias_query_lower) >= 3:
                for filepath, keywords in document_keywords.items():
                    for kw in keywords:
                        if kw.lower() in alias_query_lower or alias_query_lower in kw.lower():
                            return filepath, kw
                        
            return None, None
    except Exception:
        return None, None
