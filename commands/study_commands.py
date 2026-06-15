# commands/study_commands.py
import os
import re
from collections import Counter
import PyPDF2
from commands import file_commands
from commands import app_commands
from core import session
from core import ai_engine

def _extract_text(filepath):
    """Extensible text extraction handler."""
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == ".pdf":
        text = ""
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                limit = min(15, num_pages)
                
                for i in range(limit):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
            # Advanced PDF Content Cleaner: Remove headers, footers, watermarks, page numbers
            raw_lines = text.split('\n')
            
            # First pass: Count frequencies to find repeating headers/footers
            line_counts = Counter(line.strip() for line in raw_lines if line.strip())
            
            clean_lines = []
            for line in raw_lines:
                clean_line = line.strip()
                if not clean_line:
                    continue
                # Remove standalone page numbers (e.g. "1", "1/10", "- 5 -")
                if re.match(r'^[\-\s]*[\d/]+[\-\s]*$', clean_line):
                    continue
                # Remove repeating lines (appear > 2 times) like headers/watermarks
                if line_counts[clean_line] > 2:
                    continue
                clean_lines.append(clean_line)
                
            # Clean text to measure actual characters
            cleaned_text = "\n".join(clean_lines).strip()
            
            # Terminal logging
            print(f"Pages Scanned: {limit}/{num_pages}")
            print(f"Characters Extracted: {len(cleaned_text)}")
            
            if len(cleaned_text) < 50:
                print("AI Invocation: SKIPPED (Not enough text)")
                return None, "I could not extract readable text from this PDF. This appears to be a scanned or image-based PDF. OCR support is not yet available."
                
            return cleaned_text, None
        except Exception as e:
            return None, f"Error reading PDF: {e}"
            
    # Future support for .docx, .pptx, .txt will go here
    
    return None, f"Unsupported file type: {ext}"

def summarize_file():
    filepath = session.get_last_file()
    if not filepath or not os.path.exists(filepath):
        return "No file is currently active. Please open a PDF first."
        
    print(f"Current Document: {filepath}")
    session.set_active_context_type("document")
    text, error = _extract_text(filepath)
    
    if error:
        return error
        
    print("AI Invocation: YES")
    print("Generating summary...")
    text_capped = text[:3000]  # Cap input tokens for safe API usage
    prompt = f"Summarize the following document and provide a short 2-3 sentence overview:\n\n{text_capped}"
    
    try:
        response = ai_engine.ask_ai(prompt)
        if "quota" in response.lower() or "error" in response.lower():
            raise Exception("AI Error")
        return response
    except Exception:
        # Local fallback algorithm
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # 1. Detect document type
        text_lower = text[:1000].lower()
        doc_type = "Scanned Document/PDF"
        if "assignment" in text_lower:
            doc_type = "Assignment"
        elif "resume" in text_lower or "curriculum vitae" in text_lower:
            doc_type = "Resume"
        elif "notes" in text_lower:
            doc_type = "Notes"
            
        # 2. Extract meaningful headings (short lines)
        headings = [line for line in lines if len(line) < 40 and not line.isnumeric()][:3]
        
        # 3. Extract key lines (longer descriptive lines)
        key_lines = [line for line in lines if len(line) > 50][:4]
        
        # 4. Present concise bullet points
        fallback = "Cloud AI unavailable.\nUsing local summary mode.\n\n"
        fallback += f"Document Type: {doc_type}\n\n"
        fallback += "Key Information:\n\n"
        
        for h in headings:
            fallback += f"* {h}\n"
            
        for k in key_lines:
            # Just take the first few words of key lines to keep it concise
            words = k.split()[:7]
            fallback += f"* {' '.join(words)}...\n"
            
        return fallback.strip()

def get_key_points():
    filepath = session.get_last_file()
    if not filepath or not os.path.exists(filepath):
        return "No file is currently active. Please open a PDF first."
        
    print(f"Current Document: {filepath}")
    session.set_active_context_type("document")
    text, error = _extract_text(filepath)
    
    if error:
        return error
        
    print("AI Invocation: YES")
    print("Extracting key points...")
    text_capped = text[:3000]
    prompt = f"Extract the top 5 key points from this document as a bulleted list:\n\n{text_capped}"
    
    try:
        response = ai_engine.ask_ai(prompt)
        if "quota" in response.lower() or "error" in response.lower():
            raise Exception("AI Error")
        return response
    except Exception:
        return "Cloud AI unavailable. Could not extract key points locally."

def create_revision_notes(custom_name=None):
    filepath = session.get_last_file()
    if not filepath or not os.path.exists(filepath):
        return "No file is currently active. Please open a PDF first."
        
    print(f"Current Document: {filepath}")
    session.set_active_context_type("document")
    text, error = _extract_text(filepath)
    
    if error:
        return error
        
    print("AI Invocation: YES")
    print("Generating revision notes...")
    text = text[:3000]  # Cap input tokens for safe API usage
    prompt = f"Create concise revision notes, important concepts, and study points from this text:\n\n{text}"
    notes = ai_engine.ask_ai(prompt)
    
    if custom_name:
        notes_name = f"{custom_name.replace(' ', '_')}.txt"
    else:
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        notes_name = f"{base_name}_revision.txt"
        
    notes_path = os.path.join(file_commands.WORKSPACE_PATH, notes_name)
    
    try:
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(notes)
        session.update_last_revision_note(notes_path)
        return f"Revision notes generated and saved as {notes_name}."
    except Exception as e:
        return f"Error saving notes: {e}"

def start_study_mode():
    print("Starting study mode...")
    
    file_commands.open_system_folder("documents")
    file_commands.open_latest_file("pdf")
    app_commands.open_app("code")
        
    return "Study mode activated."
