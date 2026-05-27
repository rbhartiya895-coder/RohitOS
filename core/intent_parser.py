# core/intent_parser.py
# Normalizes input commands using defined aliases

from core.intent_aliases import INTENT_ALIASES

def normalize_intent(command_text):
    if command_text in INTENT_ALIASES:
        return INTENT_ALIASES[command_text]
        
    return command_text
