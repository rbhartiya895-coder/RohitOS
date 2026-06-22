# core/system_state.py
import time

_pending_action = None
_action_timestamp = 0
ACTION_CONFIRM_TIMEOUT = 15

def set_pending_system_action(action):
    global _pending_action, _action_timestamp
    _pending_action = action
    _action_timestamp = time.time()

def get_pending_system_action():
    global _pending_action, _action_timestamp
    if not _pending_action:
        return None
        
    if time.time() - _action_timestamp > ACTION_CONFIRM_TIMEOUT:
        _pending_action = None
        return None
        
    return _pending_action

def clear_pending_system_action():
    global _pending_action, _action_timestamp
    _pending_action = None
    _action_timestamp = 0
