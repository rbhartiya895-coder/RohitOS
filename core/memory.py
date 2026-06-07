# core/memory.py
# Persistent memory system for RohitOS

import json
import os


# -----------------------------------
# MEMORY FILE
# -----------------------------------

MEMORY_FILE = "data/memory.json"

_cache = None


# -----------------------------------
# LOAD MEMORY
# -----------------------------------

def _load_memory():

    global _cache

    # USE CACHE IF AVAILABLE
    if _cache is not None:
        return _cache

    # LOAD FILE
    if os.path.exists(MEMORY_FILE):

        try:

            with open(MEMORY_FILE, "r") as f:

                _cache = json.load(f)

                return _cache

        except Exception as e:

            print(f"Memory Load Error: {e}")

            _cache = {}

            return _cache

    # CREATE EMPTY MEMORY
    _cache = {}

    return _cache


# -----------------------------------
# SAVE MEMORY
# -----------------------------------

def _save_memory(memory):

    global _cache

    try:

        os.makedirs(
            os.path.dirname(MEMORY_FILE),
            exist_ok=True
        )

        with open(MEMORY_FILE, "w") as f:

            json.dump(
                memory,
                f,
                indent=4
            )

        # UPDATE CACHE
        _cache = memory

    except Exception as e:

        print(f"Memory Save Error: {e}")


# -----------------------------------
# REMEMBER DATA
# -----------------------------------

def remember(key, value):
    memory = _load_memory()
    key = key.lower().strip()
    memory[key] = value
    _save_memory(memory)
    return f"I will remember that your {key} is {value}"

def remember_fact(fact):
    fact = fact.strip()
    words = fact.split()
    
    if len(fact) < 10 or len(words) < 3:
        return "That fact is too short to save."
        
    memory = _load_memory()
    if "facts" not in memory:
        memory["facts"] = []
    
    if fact in memory["facts"]:
        return "I already remember that."
        
    # Store the fact
    memory["facts"].append(fact)
    _save_memory(memory)
    return "I will remember that."


# -----------------------------------
# RECALL DATA
# -----------------------------------

def recall(key):
    memory = _load_memory()
    key = key.lower().strip()
    if key in memory:
        return f"Your {key} is {memory[key]}"
    return "I don't remember that yet."


# -----------------------------------
# SHOW ALL MEMORY
# -----------------------------------

def show_memory():
    memory = _load_memory()
    if not memory:
        return "Memory is empty."

    print("\n--- SAVED MEMORY ---")
    
    # Display Key-Value pairs
    for key, value in memory.items():
        if key != "facts":
            print(f"{key.title()}: {value}")
            
    # Display Facts
    if "facts" in memory and memory["facts"]:
        print("\nFacts:")
        for fact in memory["facts"]:
            print(f"* {fact}")
            
    print("--------------------\n")
    # Calculate accurate item count
    total_items = len([k for k in memory.keys() if k != "facts"])
    if "facts" in memory:
        total_items += len(memory["facts"])
        
    return f"You have {total_items} saved items in memory."


# -----------------------------------
# FORGET DATA
# -----------------------------------

def forget(key):

    memory = _load_memory()
    key = key.lower().strip()
    
    deleted_something = False

    if key in memory:
        del memory[key]
        deleted_something = True
        
    # Check facts for partial match
    if "facts" in memory:
        original_length = len(memory["facts"])
        memory["facts"] = [f for f in memory["facts"] if key not in f.lower()]
        if len(memory["facts"]) < original_length:
            deleted_something = True

    if deleted_something:
        _save_memory(memory)
        return f"I have forgotten {key}."

    return f"I don't have anything saved for {key}."


# -----------------------------------
# CLEAR MEMORY
# -----------------------------------

def clear_memory():

    global _cache

    _cache = {}

    _save_memory({})

    return "Memory cleared."