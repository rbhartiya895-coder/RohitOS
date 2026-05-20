# commands/web_commands.py

import webbrowser


WEBSITES = {

    "google": "https://www.google.com",

    "youtube": "https://www.youtube.com",

    "github": "https://www.github.com",

    "chatgpt": "https://chat.openai.com",
"chat gpt": "https://chat.openai.com",

    "instagram": "https://www.instagram.com",

    "facebook": "https://www.facebook.com"
}


def open_website(site_name):

    site_name = site_name.lower()

    if site_name in WEBSITES:

        webbrowser.open(WEBSITES[site_name])

        print(f"Opening {site_name}")

    else:

        print("Website not recognized")