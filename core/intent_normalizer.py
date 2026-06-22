# core/intent_normalizer.py
import re

INTENT_ALIASES = {
    "summarize_page": [
        "yeh page kis bare mein hai",
        "is page ka summary do",
        "page ka summary do",
        "is article ka summary do",
        "article ka summary do",
        "page summarize karo",
        "summary batao",
        "article ke bare mein summary do",
        "is article ki summary do",
        "article summarize karo",
        "article ka summary batao"
    ],
    "get_page_key_points": [
        "main points batao",
        "important facts batao",
        "important points batao",
        "key points batao",
        "main baatein batao",
        "important baatein batao",
        "iske key points batao"
    ],
    "make_page_notes": [
        "notes banao",
        "notes save karo",
        "is page ke notes banao",
        "article ke notes banao",
        "study notes banao",
        "short notes banao"
    ],
    "save_article": [
        "article save karo",
        "page save karo"
    ],
    "shutdown_command": [
        "shutdown kar do",
        "band ho jao",
        "system band karo"
    ],
    "sleep_command": [
        "sleep mode",
        "so jao",
        "sleep par jao"
    ],
    "open_calculator": [
        "calculator kholo",
        "calculator open karo",
        "calculator chalu karo",
        "open calculator",
        "open the calculator",
        "start calculator"
    ],
    "open_browser": [
        "chrome kholo",
        "chrome open karo",
        "browser kholo",
        "google kholo",
        "open chrome",
        "open browser",
        "launch chrome"
    ],
    "open_notepad": [
        "notepad kholo",
        "notes kholo",
        "notepad open karo"
    ]
}

def normalize(command_text):
    """
    Normalizes Hindi/Hinglish commands to canonical intents.
    Returns (intent, canonical_command) or (None, original_command)
    """
    text = command_text.lower().strip()
    
    # 0. Preprocessing for STT spelling variations
    text = re.sub(r'\byah\b', 'yeh', text)
    text = re.sub(r'\bye\b', 'yeh', text)
    text = re.sub(r'\bbaare\b', 'bare', text)
    text = re.sub(r'\bke bare\b', 'kis bare', text)
    text = re.sub(r'\bartical\b', 'article', text)
    text = re.sub(r'\bsamri\b', 'summary', text)
    text = re.sub(r'\bsummry\b', 'summary', text)
    text = re.sub(r'\bcrate\b', 'create', text)
    text = re.sub(r'\bbnao\b', 'banao', text)
    text = re.sub(r'\bbnado\b', 'banao', text)
    
    # 1. Exact / Alias Matching
    for intent, aliases in INTENT_ALIASES.items():
        if text in aliases:
            return intent, text
            
    # 2. Fuzzy / Parameterized Matching for "open" operations
    # Example: "show shahrukh notes", "aadhaar card kholo"
    open_fillers = [
        r"^mera\s+", r"^mere\s+", r"\s+kholo$", r"\s+dikhao$", 
        r"\s+open karo$", r"^open\s+", r"^show\s+", r"\s+card$"
    ]
    
    is_open = False
    if "kholo" in text or "dikhao" in text or "open karo" in text or text.startswith("show ") or text.startswith("open "):
        is_open = True
        
    if is_open:
        target = text
        for pattern in open_fillers:
            target = re.sub(pattern, "", target).strip()
            
        if target:
            # Reconstruct as standard English for router parameter extraction
            canonical = f"open {target}"
            
            # Map based on target
            if "notes" in target:
                return "open_notes_file", canonical
            else:
                return "open_specific_file", canonical
                
    # 3. Fuzzy / Parameterized Matching for "close" operations
    close_fillers = [r"\s+band karo$"]
    is_close = False
    if "band karo" in text:
        is_close = True
        
    if is_close:
        target = text
        for pattern in close_fillers:
            target = re.sub(pattern, "", target).strip()
        
        if target:
            canonical = f"close {target}"
            return "close_application", canonical
                
    return None, command_text
