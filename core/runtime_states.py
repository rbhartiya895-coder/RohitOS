# core/runtime_states.py
# Centralized runtime state definitions for RohitOS

ACTIVE = "active"
SLEEPING = "sleeping"
PROCESSING = "processing"
STOPPED = "stopped"

_current_state = ACTIVE


def set_state(new_state):
    global _current_state
    _current_state = new_state


def get_state():
    return _current_state


def is_active():
    return _current_state == ACTIVE


def is_sleeping():
    return _current_state == SLEEPING


def is_processing():
    return _current_state == PROCESSING


def is_stopped():
    return _current_state == STOPPED


def state_name():
    return _current_state.upper()

_last_ux_state = None

def print_ux_state(state_str):
    global _last_ux_state
    if state_str != _last_ux_state:
        print(f"\n[STATE] {state_str}")
        _last_ux_state = state_str
