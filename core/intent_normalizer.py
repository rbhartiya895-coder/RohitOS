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
    "system_shutdown": [
        "shutdown laptop", "shutdown computer", "system band karo", "shutdown kar do"
    ],
    "system_restart": [
        "restart laptop", "restart computer", "system restart karo"
    ],
    "system_sleep": [
        "sleep laptop", "sleep computer", "sleep mode", "so jao", "sleep par jao"
    ],
    "system_lock": [
        "lock laptop", "lock computer", "system lock karo"
    ],
    "volume_up": [
        "volume up", "volume badhao"
    ],
    "volume_down": [
        "volume down", "volume kam karo"
    ],
    "volume_mute": [
        "mute", "mute karo", "silent mode"
    ],
    "volume_unmute": [
        "unmute", "sound wapas lao"
    ],
    "confirm_yes": [
        "yes", "confirm", "haan"
    ],
    "open_gmail": [
        "gmail kholo", "open gmail"
    ],
    "open_youtube": [
        "youtube kholo", "open youtube"
    ],
    "open_chatgpt": [
        "chatgpt kholo", "open chatgpt"
    ],
    "open_github": [
        "github kholo", "open github"
    ],
    "open_google": [
        "google kholo", "open google"
    ],
    "open_downloads": [
        "downloads kholo", "open downloads"
    ],
    "open_desktop": [
        "desktop kholo", "open desktop"
    ],
    "open_documents": [
        "documents kholo", "open documents"
    ],
    "open_pictures": [
        "pictures kholo", "open pictures"
    ],
    "open_videos": [
        "videos kholo", "open videos"
    ],
    "open_music": [
        "music kholo", "open music"
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
            return "close_app", canonical
                
    return None, command_text
