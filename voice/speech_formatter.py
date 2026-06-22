import re

def format_for_speech(text):
    if not text:
        return ""
    
    # 1. Replace URLs with a brief mention
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'link removed for brevity', text)
    
    # 1.5 Humanize filenames
    def _humanize(match):
        name = match.group(0)
        name = re.sub(r'\.[a-zA-Z0-9]+$', '', name) # Remove extension
        name = re.sub(r'_notes$', ' Notes', name, flags=re.IGNORECASE)
        name = name.replace('_', ' ')
        name = re.sub(r'\s+', ' ', name).strip()
        return name.title()
        
    text = re.sub(r'\b[\w\-_]+\.(?:pdf|txt|docx|pptx|doc|ppt)\b', _humanize, text, flags=re.IGNORECASE)
    
    # 2. Convert markdown bold/italics (but keep the text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
    # 2.5 Strip debug / internal messages
    debug_phrases = [
        "AI system is not configured.",
        "AI system is not configured",
        "Cache Source:",
        "Browser cache hit",
        "Cloud AI unavailable.",
        "Using local summary mode."
    ]
    for phrase in debug_phrases:
        text = text.replace(phrase, "")
        
    # 2.6 Strip AI duplicate key point intros
    text = re.sub(r'(?i)here are (the|a few|some) (key|main|important) points[:\.\-]*\s*', '', text)
    
    # 3. Handle markdown headers
    text = re.sub(r'^#+\s+(.*)$', r'\1.', text, flags=re.MULTILINE)
    
    # 4. Remove excessive repeating punctuation
    text = re.sub(r'[-_]{2,}', '', text)
    
    # 5. Format lists to sound natural
    lines = text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        clean_line = line.strip()
        # Check if line is a bullet point
        if re.match(r'^[\•\-\*]\s+', clean_line) or re.match(r'^Key Point \d+:', clean_line):
            if not in_list:
                in_list = True
                # Always add exactly one intro if not present
                formatted_lines.append("Here are the key points.")
                
            # Remove the bullet symbol and ensure it ends with punctuation
            content = re.sub(r'^[\•\-\*]\s+', '', clean_line).strip()
            if not content.endswith('.'):
                content += '.'
            formatted_lines.append(content)
        else:
            in_list = False
            if clean_line:
                formatted_lines.append(clean_line)
                
    # 6. Normalize whitespace
    final_text = " ".join(formatted_lines)
    final_text = re.sub(r'\s+', ' ', final_text).strip()
    
    # 7. Hotfix: Sarvam 500 char limit. Hard limit to 450.
    if len(final_text) > 450:
        truncated = final_text[:450]
        # Find the last sentence boundary
        match = None
        for m in re.finditer(r'[.!?](?:\s|$)', truncated):
            match = m
            
        if match:
            final_text = truncated[:match.end()].strip()
        else:
            final_text = truncated.strip() + "..."
            
    return final_text
