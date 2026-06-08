import os
import json
import time
import requests
import re
from collections import Counter
from bs4 import BeautifulSoup
from core.session import get_browser_context, update_browser_context, update_browser_cache_keys
from core.ai_engine import ask_ai
from urllib.parse import urlparse

def get_current_page():
    """
    Passively extracts the URL and title from the active Chrome/Edge window using UIAutomation.
    Fetches the HTML and extracts text. Caches in session to avoid re-fetching.
    """
    try:
        import uiautomation as auto
    except ImportError:
        return False
        
    try:
        auto.SetGlobalSearchTimeout(1.0)
        # Find foreground window
        window = auto.GetForegroundControl()
        if not window:
            return False
            
        name = window.Name
        if "Google Chrome" not in name and "Microsoft Edge" not in name:
            return False
            
        address_bar = window.EditControl()
        if not address_bar.Exists(0, 0):
            return False
            
        url = address_bar.GetValuePattern().Value
        if not url:
            return False
            
        if not url.startswith("http"):
            url = "https://" + url
            
        # Check cache
        ctx = get_browser_context()
        if ctx and ctx.get("url") == url:
            # Already cached
            return True
            
        # Fetch content
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        # Limit text length
        text = text[:8000]
        
        domain = urlparse(url).netloc
        
        # Extract headings for fallback
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]
        
        # Extract title from HTML if possible, else use window title
        page_title = soup.title.string if soup.title else name
        page_title = page_title.strip() if page_title else name
        
        update_browser_context(page_title, url, text, domain, headings=headings)
        return True
    except Exception as e:
        print(f"Error fetching page: {e}")
        return False
    finally:
        try:
            auto.SetGlobalSearchTimeout(10.0) # reset to default
        except:
            pass

def get_website_info():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage."
    return f"You are viewing {ctx['title']} at {ctx['domain']}."

def _extract_local_keywords(text):
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of", "is", "are", "was", "were", "it", "this", "that", "these", "those", "from", "as", "be", "not", "have", "has", "had", "which", "will", "can", "their", "they"}
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in stop_words]
    most_common = Counter(filtered).most_common(5)
    return [w[0] for w in most_common]

def _generate_local_key_points(summary):
    sentences = [s.strip() for s in summary.split('.') if len(s.strip()) > 5]
    return "\n".join(f"- {s}." for s in sentences)

def _get_local_summary(ctx):
    title = ctx.get('title', '')
    headings = ctx.get('headings', [])
    keywords = ctx.get('keywords', [])
    
    parts = []
    parts.append(f"Title: {title}")
    if headings:
        parts.append(f"Headings: {', '.join(headings[:3])}")
    if keywords:
        parts.append(f"Keywords: {', '.join(keywords)}")
        
    text = ctx.get('text', '')
    first_para = ". ".join(text.split('.')[:3]).strip()
    if first_para:
        parts.append(f"Summary: {first_para}.")
        
    return "\n".join(parts)

def summarize_page():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage to summarize."
        
    if ctx.get("summary"):
        print("[Browser AI Cache HIT]\nUsing cached browser context.")
        return ctx["summary"]
        
    print("[Browser AI Cache MISS]\nCalling Gemini...")
    prompt = f"Summarize this webpage content concisely in 2-3 sentences:\n\nTitle: {ctx['title']}\n\nContent:\n{ctx['text']}"
    summary = ask_ai(prompt)
    
    keywords = _extract_local_keywords(ctx['text'])
    
    if not summary or "Error" in summary:
        print("Cloud AI unavailable.\nUsing local summary mode.")
        ctx['keywords'] = keywords
        local_summary = _get_local_summary(ctx)
        update_browser_cache_keys({"keywords": keywords, "summary": local_summary})
        return local_summary
        
    update_browser_cache_keys({"keywords": keywords, "summary": summary})
    return summary

def get_key_points():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage."
        
    if ctx.get("key_points"):
        print("[Browser AI Cache HIT]\nUsing cached browser context.")
        return ctx["key_points"]
        
    if ctx.get("summary"):
        print("[Browser AI Cache HIT]\nUsing cached browser context.")
        key_points = _generate_local_key_points(ctx["summary"])
        update_browser_cache_keys({"key_points": key_points})
        return key_points
        
    print("[Browser AI Cache MISS]\nCalling Gemini...")
    prompt = f"Extract 3 to 5 key points from this webpage as a bulleted list:\n\nTitle: {ctx['title']}\n\nContent:\n{ctx['text']}"
    points = ask_ai(prompt)
    if not points or "Error" in points:
        return "Cloud AI unavailable. I cannot extract key points locally right now."
        
    update_browser_cache_keys({"key_points": points})
    return points

def make_notes():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage."
        
    notes = ""
    if ctx.get("summary") and ctx.get("key_points"):
        print("[Browser AI Cache HIT]\nUsing cached browser context.")
        notes = f"Title: {ctx['title']}\n\nSummary:\n{ctx['summary']}\n\nKey Points:\n{ctx['key_points']}"
    else:
        print("[Browser AI Cache MISS]\nCalling Gemini...")
        prompt = f"Create structured study notes from this webpage:\n\nTitle: {ctx['title']}\n\nContent:\n{ctx['text']}"
        notes = ask_ai(prompt)
        if not notes or "Error" in notes:
            return "Cloud AI unavailable. I cannot generate notes right now."
        
    # Save notes
    notes_dir = os.path.join("rohitos_workspace", "notes")
    os.makedirs(notes_dir, exist_ok=True)
    
    import re
    safe_title = re.sub(r'[^a-zA-Z0-9]', '_', ctx['title'])[:30]
    filename = f"{safe_title}_notes.txt"
    filepath = os.path.join(notes_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(notes)
            
        return f"I have saved notes from the webpage to {filename}."
    except Exception as e:
        print(f"Error saving notes: {e}")
        return "I couldn't save the notes."

def create_ppt_points():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage."
        
    if ctx.get("summary") and ctx.get("key_points"):
        print("[Browser AI Cache HIT]\nUsing cached browser context.")
        ppt = f"Slide 1: {ctx['title']}\n- {ctx['summary']}\n\nSlide 2: Key Points\n{ctx['key_points']}"
        return ppt
        
    print("[Browser AI Cache MISS]\nCalling Gemini...")
    prompt = f"Create presentation slides from this webpage. Format exactly like 'Slide 1: [Title]\\n- Point 1\\n- Point 2'. Create 3 slides.\n\nContent:\n{ctx['text']}"
    ppt = ask_ai(prompt)
    if not ppt or "Error" in ppt:
        return "Cloud AI unavailable."
    return ppt

def save_article():
    ctx = get_browser_context()
    if not ctx:
        return "I cannot detect an active webpage."
        
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    saved_file = os.path.join(data_dir, "saved_articles.json")
    
    articles = []
    if os.path.exists(saved_file):
        try:
            with open(saved_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except Exception:
            pass
            
    articles.append({
        "title": ctx.get("title", ""),
        "url": ctx.get("url", ""),
        "domain": ctx.get("domain", ""),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": ctx.get("summary", ""),
        "keywords": ctx.get("keywords", [])
    })
    
    with open(saved_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)
        
    return f"I have saved the article {ctx.get('title', 'Unknown')}."

def show_saved_articles():
    saved_file = os.path.join("data", "saved_articles.json")
    if not os.path.exists(saved_file):
        return "You have no saved articles."
        
    try:
        with open(saved_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
            
        if not articles:
            return "You have no saved articles."
            
        output = []
        for i, article in enumerate(articles, 1):
            title = article.get("title", "Unknown Article")
            output.append(f"{i}. {title}")
            
        return "\n".join(output)
    except Exception as e:
        return "Error reading saved articles."
