# commands/search_commands.py
# Handles browser search commands.

import webbrowser
import urllib.parse


# -----------------------------------
# HELPER FUNCTIONS
# -----------------------------------

def clean_search_query(query):
    return " ".join(query.split())


# -----------------------------------
# GOOGLE SEARCH
# -----------------------------------

def search_google(query):

    query = clean_search_query(query)
    encoded_query = urllib.parse.quote(query)

    url = (
        f"https://www.google.com/search?q="
        f"{encoded_query}"
    )

    webbrowser.open(url)

    print(f"Searching Google for: {query}")

    return f"Searching Google for {query}"


# -----------------------------------
# YOUTUBE SEARCH
# -----------------------------------

def search_youtube(query):

    query = clean_search_query(query)
    encoded_query = urllib.parse.quote(query)

    url = (
        f"https://www.youtube.com/results?search_query="
        f"{encoded_query}"
    )

    webbrowser.open(url)

    print(f"Searching YouTube for: {query}")

    return f"Searching YouTube for {query}"