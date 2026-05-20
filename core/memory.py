# core/memory.py
# Persistent memory system for RohitOS.
import json
import os

MEMORY_FILE = "data/memory.json"

def _load_memory():
    """Loads memory from the JSON file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_memory(memory):
    """Saves memory to the JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def remember(key, value):
    """Stores a key-value pair in memory."""
    memory = _load_memory()
    memory[key] = value
    _save_memory(memory)
    return f"Remembered: {key} as {value}"

def recall(key):
    """Recalls a value associated with a key from memory."""
    memory = _load_memory()
    return memory.get(key, "")

def show_all_memory():
    """Returns all stored memory."""
    return _load_memory()
