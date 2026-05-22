# core/state_manager.py
# Handles assistant state management


# -----------------------------------
# ASSISTANT STATES
# -----------------------------------

ACTIVE = "active"

SLEEPING = "sleeping"

SHUTDOWN = "shutdown"


# -----------------------------------
# CURRENT STATE
# -----------------------------------

assistant_state = ACTIVE


# -----------------------------------
# STATE FUNCTIONS
# -----------------------------------

def set_state(new_state):

    global assistant_state

    assistant_state = new_state


def get_state():

    return assistant_state


# -----------------------------------
# STATE CHECKS
# -----------------------------------

def is_active():

    return assistant_state == ACTIVE


def is_sleeping():

    return assistant_state == SLEEPING


def is_shutdown():

    return assistant_state == SHUTDOWN