import re

def format_for_speech(text):
    if not text:
        return ""
    
    # 1. Replace URLs with a brief mention
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'link removed for brevity', text)
    
    # 2. Convert markdown bold/italics (but keep the text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
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
        if re.match(r'^[\•\-\*]\s+', clean_line):
            if not in_list:
                in_list = True
                # Only prepend if not already stated
                if not any("here are the key points" in l.lower() for l in formatted_lines[-3:]):
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
    
    return final_text
