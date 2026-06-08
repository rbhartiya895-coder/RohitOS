# core/session.py
import os
import json
import re

SESSION_FILE = os.path.join("data", "session.json")
_MEMORY_CACHE = None
_LAST_MTIME = 0

def _load_cache():
    global _MEMORY_CACHE, _LAST_MTIME
    current_mtime = 0
    if os.path.exists(SESSION_FILE):
        try:
            current_mtime = os.path.getmtime(SESSION_FILE)
        except OSError:
            pass
            
    # Invalidate if file changed externally
    if _MEMORY_CACHE is not None and current_mtime == _LAST_MTIME:
        return _MEMORY_CACHE
        
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _MEMORY_CACHE = json.load(f)
                _LAST_MTIME = current_mtime
        except Exception:
            _MEMORY_CACHE = {}
    else:
        _MEMORY_CACHE = {}
    return _MEMORY_CACHE

def _save_cache():
    global _MEMORY_CACHE, _LAST_MTIME
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(_MEMORY_CACHE, f, indent=4)
        _LAST_MTIME = os.path.getmtime(SESSION_FILE)
    except Exception as e:
        print(f"Error saving session: {e}")

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

def _update_session_keys(updates):
    _ensure_data_dir()
    data = _load_cache()
    if "aliases" not in data:
        data["aliases"] = {}
    if "document_keywords" not in data:
        data["document_keywords"] = {}
            
    for key, value in updates.items():
        data[key] = value
        
        if key == "last_opened_file":
            filename = os.path.basename(value)
            aliases = generate_aliases(filename)
            for alias in aliases:
                if alias not in data["aliases"] and len(data["aliases"]) >= 100:
                    first_key = next(iter(data["aliases"]))
                    del data["aliases"][first_key]
                data["aliases"][alias] = value
        
    _save_cache()

def _update_session_key(key, value):
    _update_session_keys({key: value})

def update_last_file(filepath):
    _update_session_keys({"last_opened_file": filepath, "active_context_type": "document"})

def set_active_context_type(context_type):
    _update_session_key("active_context_type", context_type)

def get_active_context_type():
    data = _load_cache()
    return data.get("active_context_type", "document")

def store_document_keywords(filepath, keywords):
    _ensure_data_dir()
    data = _load_cache()
    if "document_keywords" not in data:
        data["document_keywords"] = {}
            
    data["document_keywords"][filepath] = keywords
    _save_cache()

def get_last_file():
    data = _load_cache()
    return data.get("last_opened_file")

def update_last_revision_note(filepath):
    _update_session_key("last_revision_note", filepath)

def get_last_revision_note():
    data = _load_cache()
    return data.get("last_revision_note")

def get_document_alias(alias_query):
    """Lookup a filepath by an exact, fuzzy, or keyword match."""
    data = _load_cache()
    aliases = data.get("aliases", {})
    document_keywords = data.get("document_keywords", {})
    
    alias_query_lower = alias_query.lower()
    
    # Exact match
    if alias_query_lower in aliases:
        return aliases[alias_query_lower], alias_query_lower, "alias"
        
    # Fuzzy match aliases
    matches = difflib.get_close_matches(alias_query_lower, aliases.keys(), n=1, cutoff=0.6)
    if matches:
        return aliases[matches[0]], matches[0], "alias"
        
    # Keyword match
    if len(alias_query_lower) >= 3:
        for filepath, keywords in document_keywords.items():
            for kw in keywords:
                if kw.lower() in alias_query_lower or alias_query_lower in kw.lower():
                    return filepath, kw, "keyword"
                
    return None, None, None

def update_browser_context(title, url, text, domain, headings=None):
    import time
    _ensure_data_dir()
    data = _load_cache()
            
    data["browser_context"] = {
        "title": title,
        "url": url,
        "text": text[:8000],
        "domain": domain,
        "timestamp": time.time(),
        "headings": headings or [],
        "summary": None,
        "key_points": None,
        "keywords": None
    }
    data["active_context_type"] = "browser"
    
    _save_cache()

def get_browser_context():
    data = _load_cache()
    return data.get("browser_context")

def update_browser_cache_keys(updates):
    _ensure_data_dir()
    data = _load_cache()
            
    if "browser_context" not in data or not isinstance(data["browser_context"], dict):
        data["browser_context"] = {}
        
    for k, v in updates.items():
        data["browser_context"][k] = v
        
    _save_cache()
