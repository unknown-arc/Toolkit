import json
from pathlib import Path

class GetAppInfo:
    def __init__(self, app_id, profile_path: Path):
        self.app_id = app_id
        self.profile_path = profile_path

    def get_app_info(self, app_id=None, profile_path: Path = None):
        # Fallback to instance values
        app_id = app_id or self.app_id
        profile_path = profile_path or self.profile_path

        if profile_path is None:
            raise ValueError("profile_path cannot be None")

        apps_file = (
            profile_path / "data" / "json_data" / "subapps.json"
        )

        if not apps_file.exists():
            raise FileNotFoundError(f"{apps_file} not found")

        with open(apps_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get(app_id)
