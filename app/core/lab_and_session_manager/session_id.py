# core/session_id.py

import uuid
from typing import NewType

# Define a custom type for better code clarity and type hinting
SessionID = NewType('SessionID', str)

def generate_session_id() -> SessionID:
    """
    Generates a unique, collision-free Session ID using UUID version 4.
    This ID tracks the lifecycle of user interaction within a lab.
    """
    return SessionID(str(uuid.uuid4()))