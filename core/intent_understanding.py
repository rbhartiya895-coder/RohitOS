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
    "download": "open downloads",
    "downloads": "open downloads",
    "download folder": "open downloads",
    "downloads folder": "open downloads",
    "my download folder": "open downloads",
    "my downloads folder": "open downloads",
    "open download": "open downloads",
    "documents": "open documents",
    "desktop": "open desktop",
    "pictures": "open pictures",
    "my downloads": "open downloads",
    "show my recent files": "show recent files",
    "my recent files": "show recent files",
    "recent files": "show recent files",
    "open recent pdf": "open latest pdf",
    "recent pdf": "open latest pdf",
    "memory": "show memory",
    "what do you remember about me": "show memory",
    "what do you know about me": "show memory",
    "summarize this pdf": "summarize file",
    "summarise this pdf": "summarize file",
    "what is this pdf about": "summarize file",
    "what is this pdf is about": "summarize file",
    "tell me about this pdf": "summarize file",
    "explain this pdf": "summarize file",
    "give me key points": "generic_key_points",
    "give me key points of this pdf": "summarize file",
    "create revision notes": "create revision notes",
    "make study notes from this pdf": "create revision notes",
    "summarize this": "generic_summarize",
    "summarise this": "generic_summarize",
    "make notes": "generic_make_notes",
    "open the pdf i opened earlier": "open previous document",
    "open the document i was reading": "open previous document",
    "open previous document": "open previous document",
    "open the pdf i was reading": "open previous document",
    "open document i was reading": "open previous document",
    "what website is this": "get website info",
    "where am i": "get website info",
    "current page": "get website info",
    "what page am i viewing": "get website info",
    "summarize this page": "summarize page",
    "summarise this page": "summarize page",
    "summarise page": "summarize page",
    "summarise webpage": "summarize page",
    "summarise article": "summarize page",
    "summarise": "generic_summarize",
    "what this page is about": "summarize page",
    "what is this page about": "summarize page",
    "what is this article about": "summarize page",
    "tell me about this page": "summarize page",
    "explain this page": "summarize page",
    "give me key points of this page": "get page key points",
    "important facts": "get page key points",
    "tell me keywords": "extract_keywords",
    "voice status": "voice_status",
    "main takeaways": "get page key points",
    "give me keynotes": "get page key points",
    "keynotes": "get page key points",
    "key notes": "get page key points",
    "main points": "get page key points",
    "highlights": "get page key points",
    "make notes from this page": "make_page_notes",
    "save notes from this article": "make_page_notes",
    "save notes from this page": "make_page_notes",
    "save webpage notes": "make_page_notes",
    "save article notes": "make_page_notes",
    "create notes from this page": "make_page_notes",
    "create ppt points from this page": "create ppt points",
    "presentation points": "create ppt points",
    "make ppt": "create ppt points",
    "make ppt points": "create ppt points",
    "make ppt point from this page": "create ppt points",
    "create ppt": "create ppt points",
    "ppt points": "create ppt points",
    "ppt point": "create ppt points",
    "create ppt points": "create ppt points",
    "presentation bullets": "create ppt points",
    "save this article": "save article",
    "save this webpage": "save article",
    "show saved articles": "show saved articles",
    "list saved articles": "show saved articles",
    "what articles have i saved": "show saved articles",
    "saved articles": "show saved articles"
}

def normalize_intent(command_text):
    command_text = command_text.lower().strip()
    
    # Handle PDF open variants
    if command_text.startswith("pdf open "):
        command_text = command_text.replace("pdf open ", "open ", 1)
    elif command_text.startswith("open pdf "):
        command_text = command_text.replace("open pdf ", "open ", 1)
    
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
