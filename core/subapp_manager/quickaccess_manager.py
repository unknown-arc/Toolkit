from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Optional
import tempfile
import shutil


class QuickAccessManager:
    """
    Maintains quickaccess.json mapped from subapps.json.

    Structure of quickaccess.json:
    {
        "app_id": {
            "visible": true/false,
            "index": int
        },
        ...
    }

    Rules:
    - If quickaccess.json missing → create it.
    - If new apps exist in subapps.json → add them with defaults (visible=True, index=auto).
    - If apps removed from subapps.json → remove them.
    """

    FILENAME = "quickaccess.json"

    def __init__(self, profile_path: Path):
        self.profile_path = profile_path.resolve()
        self.quick_file = self.profile_path / "data" / "json_data" / self.FILENAME
        self.subapp_file = self.profile_path / "data" / "json_data" / "subapps.json"
        print(self.quick_file, self.subapp_file)

        self._data: Dict[str, Dict[str, int | bool]] = {}

        self.load_or_rebuild()

    # ---------------------------------------------------
    # Load or rebuild quickaccess.json
    # ---------------------------------------------------
    def load_or_rebuild(self):
        """Load quickaccess.json or rebuild from subapps.json."""
        if not self.subapp_file.exists():
            print("[QuickAccess] ERROR: subapps.json not found")
            self._data = {}
            return

        subapps = json.loads(self.subapp_file.read_text(encoding="utf-8"))

        if not self.quick_file.exists():
            print("[QuickAccess] quickaccess.json not found → creating with defaults...")
            self._data = self._create_default(subapps)
            self._atomic_save()
            return

        try:
            qa_data = json.loads(self.quick_file.read_text(encoding="utf-8"))
            if not isinstance(qa_data, dict):
                raise ValueError("quickaccess.json root must be dict")
            self._data = qa_data
        except Exception as e:
            print(f"[QuickAccess] Failed to load quickaccess.json ({e}), rebuilding...")
            self._data = self._create_default(subapps)
            self._atomic_save()
            return

        changed = self._sync_with_subapps(subapps)
        if changed:
            self._atomic_save()

    # ---------------------------------------------------
    # Default creation when file missing
    # ---------------------------------------------------
    def _create_default(self, subapps: dict) -> Dict[str, dict]:
        """Create quickaccess.json with all apps = visible+indexed."""
        data = {}
        index = 0
        for app_id in subapps:
            data[app_id] = {
                "visible": True,
                "index": index
            }
            index += 1
        return data

    # ---------------------------------------------------
    # Sync subapps.json → quickaccess.json
    # ---------------------------------------------------
    def _sync_with_subapps(self, subapps: dict) -> bool:
        """Add missing apps, remove deleted apps. Reassign indexes only when needed."""

        changed = False

        # Remove deleted apps
        for app_id in list(self._data.keys()):
            if app_id not in subapps:
                self._data.pop(app_id)
                changed = True

        # Add new apps with defaults
        existing_indexes = {d["index"] for d in self._data.values()} if self._data else set()
        next_index = 0
        while next_index in existing_indexes:
            next_index += 1

        for app_id in subapps:
            if app_id not in self._data:
                self._data[app_id] = {
                    "visible": True,
                    "index": next_index
                }
                next_index += 1
                changed = True

        return changed

    # ---------------------------------------------------
    # Save (atomic)
    # ---------------------------------------------------
    def _atomic_save(self):
        tmp_fd, tmp_path = tempfile.mkstemp(prefix="quick_", suffix=".json", dir=str(self.profile_path))
        try:
            with open(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            shutil.move(tmp_path, str(self.quick_file))
        except Exception:
            self.quick_file.write_text(json.dumps(self._data, indent=4, ensure_ascii=False), encoding="utf-8")
        finally:
            p = Path(tmp_path)
            if p.exists():
                try:
                    p.unlink()
                except:
                    pass

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------
    def get_all(self):
        return dict(self._data)

    def set_visible(self, app_id: str, visible: bool):
        if app_id in self._data:
            self._data[app_id]["visible"] = visible
            self._atomic_save()
            return True
        return False

    def set_index(self, app_id: str, index: int):
        if app_id in self._data:
            self._data[app_id]["index"] = index
            self._atomic_save()
            return True
        return False

if __name__ == "__main__":
    # Simple test
    profile = Path(__file__).resolve().parent.parent.parent.parent / "data" / "Profile-2"
    qam = QuickAccessManager(profile)
    print(qam.get_all())