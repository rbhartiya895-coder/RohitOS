# commands/web_commands.py

import webbrowser


def open_website(url):

    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com"
    }

    url = url.lower()

    if url in websites:
        webbrowser.open(websites[url])
        return f"Opened {url}"

    return "Website not found"