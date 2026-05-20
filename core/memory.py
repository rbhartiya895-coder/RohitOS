# core/memory.py
# Persistent memory system for RohitOS.

import json
import os

MEMORY_FILE = "data/memory.json"

_cache = None


def _load_memory():
    """Loads memory from the JSON file."""

    global _cache

    if _cache is not None:
        return _cache

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as f:

            _cache = json.load(f)

            return _cache

    _cache = {}

    return _cache


def _save_memory(memory):
    """Saves memory to the JSON file."""

    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w") as f:

        json.dump(memory, f, indent=4)


def remember(key, value):
    """Stores a key-value pair in memory."""

    memory = _load_memory()

    memory[key] = value

    _save_memory(memory)

    return f"I will remember that {key} is {value}"


def recall(key):
    """Recalls a value associated with a key from memory."""

    memory = _load_memory()

    if key in memory:

        return f"Your {key} is {memory[key]}"

    else:

        return "I don't remember that yet."


def show_all_memory():
    """Returns all stored memory."""

    return _load_memory()