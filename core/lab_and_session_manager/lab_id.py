# core/lab_id.py

import uuid
from typing import NewType

LabID = NewType('LabID', str)

def generate_lab_id() -> LabID:
    """
    Generates a unique, collision-free Lab ID using UUID version 4.
    """
    return LabID(str(uuid.uuid4()))