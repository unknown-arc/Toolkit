# quick_lab/quick_lab_session_manager.py

from core.lab_id import LabID
from core.session_id import SessionID
from typing import Optional

# Assume LabController is imported and accessible (or passed in)
# from core.lab_controller import LabController 
# Assume Lab_eb is imported and accessible
# from core.signal_manager import Lab_eb 

class QuickLabSessionManager:
    """
    Acts as a broker between the QuickLab widget and the LabController/Signal Manager.
    Handles the generation and assignment of unique IDs upon interaction.
    """
    
    def __init__(self, lab_id: LabID, lab_controller):
        # 1. Unique IDs
        self.lab_id: LabID = lab_id
        self.session_id: Optional[SessionID] = None # Starts None, generated on first message
        
        # 2. Communication Link
        self.controller = lab_controller # Reference to the LabController
        
        # 3. Rename State (Mirrors the QuickLab flag)
        self.is_named = False

    def on_first_message(self):
        """
        Called by QuickLab when the user sends the first message.
        Generates Session ID and triggers rename in the LabController.
        """
        if not self.is_named:
            # 1. Generate Session ID via the Controller's method
            new_session_id = self.controller.start_interaction(self.lab_id)
            if new_session_id:
                self.session_id = new_session_id

            # 2. Trigger Rename Signal (using the controller's dependency on Lab_eb)
            # This is where the LabController's signal dependency is hidden from QuickLab
            if self.session_id:
                # Assuming the controller handles the Lab_eb.rename_lab_title.emit based on its state
                # Or, if the signal must be emitted here:
                from core.signal_manager import Lab_eb # Must be available
                
                Lab_eb.rename_lab_title.emit(
                    self.lab_id, 
                    self.session_id
                )
                self.is_named = True
                
            return self.session_id
        
        return self.session_id

    def get_session_code(self):
        """Quick access for QuickLab's original self.session_code property."""
        # Use a placeholder if session_id hasn't been generated yet
        return self.session_id if self.session_id else "N/A"