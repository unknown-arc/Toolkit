# core/persistence_manager.py
import json
from signal_manager import Save_eb 
from pathlib import Path

class ActivityManager:
    def __init__(self):        
        # Save_eb.save_session_req.connect(self.save_project_to_json)
        Save_eb.save_session_req.connect(print"**Persistence Request**: Saving project state to JSON")
        self.current_file_path = Path(__file__).resolve()
        self.project_root = self.current_file_path.parent.parent.parent
        self.filepath = self.project_root / "user_data"/ "Profile-2"/ "activity" / "user_activity.json"
    def save_project_to_json(self, data: dict):
        """Receives project data and writes it to the specified file path."""
        print(f"**Persistence Request**: Saving project state to {self.filepath}")
        try:
        #     filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4) 
                
            print(f"**Persistence Success**: Project state saved via signal to: {filepath}")
        except Exception as e:
            print(filepath)
            print(f"Persistence Failed: Error saving project file: {e}")

    def load_project_from_json(self) -> dict:
        """Reads project data from a JSON file and returns it as a dictionary."""
        filepath = self.filepath
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"**Persistence Success**: Project state loaded from: {filepath}")
            return data

        except Exception as e:
            print(f"Persistence Failed: Error loading project file: {e}")
            return {}

