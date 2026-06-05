# core/intent_understanding.py
# Normalizes conversational input into deterministic RohitOS commands


# 1. Strip Conversational Prefix Fillers
PREFIXES = [
    "please ", "can you ", "could you ", "would you ", 
    "i need a ", "i need ", "i want to ", "i want ", 
    "show me my ", "show me ", "open my ", "find my ", 
    "let me see my ", "let me see ", "take me to ", "help me open "
]

# 2. Strip Conversational Suffix Fillers
SUFFIXES = [" for me", " right now"]

# 3. Lightweight Intent Mappings (Deterministic)
MAPPINGS = {
    "calculator": "open calculator",
    "youtube": "open youtube",
    "downloads": "open downloads",
    "documents": "open documents",
    "desktop": "open desktop",
    "pictures": "open pictures",
    "downloads folder": "open downloads",
    "my downloads": "open downloads",
    "show my recent files": "show recent files",
    "my recent files": "show recent files",
    "recent files": "show recent files",
    "memory": "show memory",
    "what do you remember about me": "show memory",
    "what do you know about me": "show memory",
    "summarize this pdf": "summarize file",
    "summarise this pdf": "summarize file",
    "what is this pdf about": "summarize file",
    "tell me about this pdf": "summarize file",
    "give me key points": "summarize file",
    "give me key points of this pdf": "summarize file",
    "create revision notes": "create revision notes",
    "make study notes from this pdf": "create revision notes"
}

def normalize_intent(command_text):
    command_text = command_text.lower().strip()
    
    # Iteratively strip prefixes in case of stacked fillers (e.g. "please can you")
    stripped_something = True
    while stripped_something:
        stripped_something = False
        for prefix in PREFIXES:
            if command_text.startswith(prefix):
                command_text = command_text[len(prefix):].strip()
                stripped_something = True
                break
                
    for suffix in SUFFIXES:
        if command_text.endswith(suffix):
            command_text = command_text[:-len(suffix)].strip()
            
    if command_text in MAPPINGS:
        command_text = MAPPINGS[command_text]
        
    # 4. Search Pattern Normalization
    if command_text.startswith("search "):
        # If it's a search but doesn't explicitly specify a platform, default to Google
        if " on google" not in command_text and " on youtube" not in command_text:
            command_text = command_text + " on google"
            
    return command_text
