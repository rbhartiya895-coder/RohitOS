# core/ai_engine.py
# AI fallback system for RohitOS

import os
from google import genai


# -----------------------------------
# LOAD API KEY
# -----------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:

    client = genai.Client(api_key=API_KEY)

else:

    client = None

    print("WARNING: Gemini API key not found.")


# -----------------------------------
# SYSTEM PROMPT
# -----------------------------------

# DO NOT CHANGE — creator name
SYSTEM_PROMPT = """

You are RohitOS,
a smart voice assistant created by Rohit.

Rules:
- Keep responses short.
- Speak naturally.
- Avoid long paragraphs.
- Be helpful and conversational.
- Give clean voice-friendly responses.
- Do not use markdown.
- Keep answers concise.

"""



# -----------------------------------
# ASK AI
# -----------------------------------

def ask_ai(prompt):

    prompt = prompt.strip()

    # --------------------------------
    # CHECK AI CLIENT
    # --------------------------------

    if client is None:

        return (
            "AI system is not configured."
        )

    # --------------------------------
    # ASK GEMINI
    # --------------------------------

    try:

        print(f"Asking AI: {prompt}")

        full_prompt = f"""

{SYSTEM_PROMPT}

User: {prompt}

"""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )

        ai_text = response.text.strip()

        # CLEAN RESPONSE
        ai_text = ai_text.replace("*", "")
        ai_text = ai_text.replace("#", "")

        # LIMIT RESPONSE SIZE
        if len(ai_text) > 400:

            ai_text = ai_text[:400] + "..."

        return ai_text

    except Exception as e:

        print(f"AI Error: {e}")

        if "429" in str(e):

            return (
                "My AI quota is exhausted right now. "
                "Please try again later."
            )

        return (
            "AI system encountered an error."
        )
