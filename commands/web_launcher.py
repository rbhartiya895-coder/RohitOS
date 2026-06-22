# commands/web_launcher.py
import webbrowser

WEBSITES = {
    "gmail": "https://mail.google.com",
    "youtube": "https://youtube.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "google": "https://google.com"
}

def open_website(site_name):
    site_name = site_name.lower()
    if site_name in WEBSITES:
        webbrowser.open(WEBSITES[site_name])
        return f"Opening {site_name}."
    else:
        return "Website not recognized."
