# commands/study_commands.py
import os
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
                        
            if not text.strip():
                return None, "This PDF appears to be scanned or contains no extractable text."
                
            return text, None
        except Exception as e:
            return None, f"Error reading PDF: {e}"
            
    # Future support for .docx, .pptx, .txt will go here
    
    return None, f"Unsupported file type: {ext}"

def summarize_file():
    filepath = session.get_last_file()
    if not filepath or not os.path.exists(filepath):
        return "No file is currently active. Please open a PDF first."
        
    print(f"Reading file: {filepath}")
    text, error = _extract_text(filepath)
    
    if error:
        return error
        
    print("Generating summary...")
    text = text[:3000]  # Cap input tokens for safe API usage
    prompt = f"Summarize the following document and provide key takeaways in bullet points:\n\n{text}"
    return ai_engine.ask_ai(prompt)

def create_revision_notes():
    filepath = session.get_last_file()
    if not filepath or not os.path.exists(filepath):
        return "No file is currently active. Please open a PDF first."
        
    print(f"Reading file: {filepath}")
    text, error = _extract_text(filepath)
    
    if error:
        return error
        
    print("Generating revision notes...")
    text = text[:3000]  # Cap input tokens for safe API usage
    prompt = f"Create concise revision notes, important concepts, and study points from this text:\n\n{text}"
    notes = ai_engine.ask_ai(prompt)
    
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    notes_name = f"{base_name}_revision.txt"
    notes_path = os.path.join(file_commands.WORKSPACE_PATH, notes_name)
    
    try:
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(notes)
        return f"Revision notes generated and saved as {notes_name}."
    except Exception as e:
        return f"Error saving notes: {e}"

def start_study_mode():
    print("Starting study mode...")
    
    file_commands.open_system_folder("documents")
    file_commands.open_latest_file("pdf")
    app_commands.open_app("code")
        
    return "Study mode activated."
