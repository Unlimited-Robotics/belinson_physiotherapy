from src.FSMs.nurse_aid.constants.navigation_constants import *

STATES = [
    'SETUP',
    'NAVIGATING_TO_ROOM',
    'APPROACHING_PERSON',
    # 'APPROACHING_FEET', 
    'USER_SETUP', 
    'BRIEF',
    'SESSIONS', 
    'NAVIGATING_HOME',
    'END',
    'TREATMENT_PAUSE',
    'DEBUG',
    'IDLE'
]

INITIAL_STATE = 'SETUP'

END_STATES = ['END']

STATES_TIMEOUTS = {
    'LOCALIZING': LOCALIZING_TIMEOUT,
}

# Debug flag to start at a specific state
debug = False
if debug:
    INITIAL_STATE = 'DEBUG'