# app/core/subapp_manager/subapp_manage.py
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
import tempfile


class SubAppManager:
    """
    Manage profile-based subapp registry stored at <profile>/apps.json
    Scans both main_subapp and load_subapp folders in project root/Subapp
    Only requires main.py + info.json (id & name). Icon optional.
    """

    APPS_FILENAME = "subapps.json"
    SUBAPP_FOLDERS = ["main_subapp", "load_subapp"]
    INFO_FOLDERNAME = "appinfoft"
    INFO_FILENAME = "info.json"

    def __init__(self, profile_path: Path):
        self.profile_path = profile_path.resolve()
        self.apps_file = self.profile_path / "data" /"json_data" /self.APPS_FILENAME

        # Determine root folder from manager location
        self.project_root = Path(__file__).resolve().parents[3]  # App/core/subapp_manager -> Root Dir
        self.subapps_root = self.project_root /"subapp"
        print(f"[SubAppProfileManager] Project root: {self.project_root}")
        print(f"[SubAppProfileManager] Subapps root: {self.subapps_root}")

        self._data: Dict[str, Dict[str, str]] = {}

        # Load existing apps.json or rebuild from scan
        self.load_or_rebuild()

    # -------------------------
    # Public methods
    # -------------------------
    def get_apps(self) -> Dict[str, Dict[str, str]]:
        return dict(self._data)

    def get_app(self, app_id: str) -> Optional[Dict[str, str]]:
        return self._data.get(app_id)

    # -------------------------
    # Load / Save
    # -------------------------
    def load_or_rebuild(self):
        if not self.apps_file.exists():
            print("[SubAppProfileManager] apps.json not found, scanning subapps...")
            self._data = {}
            self.rebuild_from_scan()
            return

        try:
            data = json.loads(self.apps_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("apps.json root must be dict")
            self._data = data
        except Exception as e:
            print(f"[SubAppProfileManager] Failed to load apps.json ({e}), rebuilding...")
            self._data = {}
            self.rebuild_from_scan()
            return

        removed = self._validate_and_clean()
        if removed:
            print(f"[SubAppProfileManager] Removed invalid apps from apps.json: {removed}")
            self._atomic_save()

    def _atomic_save(self):
        tmp_fd, tmp_path = tempfile.mkstemp(prefix="apps_", suffix=".json", dir=str(self.profile_path))
        try:
            with open(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            shutil.move(tmp_path, str(self.apps_file))
        except Exception:
            self.apps_file.write_text(json.dumps(self._data, indent=4, ensure_ascii=False), encoding="utf-8")
        finally:
            if Path(tmp_path).exists():
                try:
                    Path(tmp_path).unlink()
                except Exception:
                    pass

    # -------------------------
    # Validation / Scan
    # -------------------------
    def _validate_and_clean(self) -> list:
        removed = []
        for app_id, meta in list(self._data.items()):
            main_path = Path(meta.get("main", ""))
            info_path = Path(meta.get("info", ""))
            icon_path = Path(meta.get("icon", "")) if meta.get("icon") else None

            if not main_path.exists() or not info_path.exists():
                print(f"[SubAppProfileManager] Removing {app_id}: main.py or info.json missing")
                removed.append(app_id)
                self._data.pop(app_id, None)
                continue

            try:
                info_obj = json.loads(info_path.read_text(encoding="utf-8"))
                if not {"id", "name"}.issubset(info_obj.keys()):
                    print(f"[SubAppProfileManager] Removing {app_id}: info.json missing required keys")
                    removed.append(app_id)
                    self._data.pop(app_id, None)
            except Exception:
                print(f"[SubAppProfileManager] Removing {app_id}: info.json corrupt")
                removed.append(app_id)
                self._data.pop(app_id, None)

        return removed

    def rebuild_from_scan(self) -> Dict[str, Dict[str, str]]:
        """
        Scan main_subapp and load_subapp folders.
        Only folders with main.py + info.json (with id & name) are added.
        Icon optional.
        """
        found = {}

        for subfolder_name in self.SUBAPP_FOLDERS:
            folder_root = self.subapps_root / subfolder_name
            if not folder_root.exists():
                print(f"[SubAppProfileManager] Subapp folder missing: {folder_root}")
                continue

            for folder in sorted(folder_root.iterdir()):
                if not folder.is_dir():
                    continue

                print(f"[SubAppProfileManager] Scanning subapp: {folder.name}")
                main_file = folder / "main.py"
                info_folder = folder / self.INFO_FOLDERNAME
                info_file = info_folder / self.INFO_FILENAME
                icon_file = None

                # optional icon: pick first file that is not info.json
                if info_folder.exists():
                    for f in info_folder.iterdir():
                        if f.is_file() and f.name != self.INFO_FILENAME:
                            icon_file = f
                            break

                if not main_file.exists() or not info_file.exists():
                    print(f"  Skipping {folder.name}: main.py or info.json missing")
                    continue

                name, info_obj = self._read_info_json(info_file)
                if not info_obj:
                    print(f"  Skipping {folder.name}: info.json missing id/name")
                    continue

                app_id = info_obj["id"].lower()
                entry = {
                    "main": str(main_file.resolve()),
                    "info": str(info_file.resolve()),
                    "id": info_obj["id"],
                    "name": info_obj["name"]
                }
                if icon_file:
                    entry["icon"] = str(icon_file.resolve())

                found[app_id] = entry
                print(f"  Added {app_id}: main.py + info.json{', icon found' if icon_file else ''}")

        self._data = found
        self._atomic_save()
        print(f"[SubAppProfileManager] Rebuilt apps.json with {len(found)} apps")
        return found

    def _read_info_json(self, info_file: Path) -> Tuple[Optional[str], Optional[Any]]:
        try:
            obj = json.loads(info_file.read_text(encoding="utf-8"))
            if not {"id", "name"}.issubset(obj.keys()):
                return None, None
            return obj["name"], obj
        except Exception:
            return None, None

    # -------------------------
    # Add / Remove API
    # -------------------------
    def add_app(self, subapp_folder: Path) -> Tuple[bool, str]:
        subapp_folder = Path(subapp_folder).resolve()
        if not subapp_folder.exists() or not subapp_folder.is_dir():
            return False, f"Folder not found: {subapp_folder}"

        main_file = subapp_folder / "main.py"
        info_file = subapp_folder / self.INFO_FOLDERNAME / self.INFO_FILENAME
        icon_file = None
        info_folder = subapp_folder / self.INFO_FOLDERNAME

        if info_folder.exists():
            for f in info_folder.iterdir():
                if f.is_file() and f.name != self.INFO_FILENAME:
                    icon_file = f
                    break

        if not main_file.exists() or not info_file.exists():
            return False, "Invalid subapp folder: main.py or info.json missing"

        name, info_obj = self._read_info_json(info_file)
        if not info_obj:
            return False, "info.json missing required keys (id, name)"

        app_id = info_obj["id"].lower()
        entry = {
            "main": str(main_file.resolve()),
            "info": str(info_file.resolve()),
            "id": info_obj["id"],
            "name": info_obj["name"]
        }
        if icon_file:
            entry["icon"] = str(icon_file.resolve())

        self._data[app_id] = entry
        self._atomic_save()
        return True, f"App '{app_id}' added"

    def remove_app(self, app_id: str) -> Tuple[bool, str]:
        app_id = app_id.lower()
        if app_id not in self._data:
            return False, "App not found in profile"
        self._data.pop(app_id, None)
        self._atomic_save()
        return True, f"Removed '{app_id}'"


# -------------------------
# TEST EXAMPLE
# -------------------------
if __name__ == "__main__":
    test_profile = Path("Z:/Project/Toolkit/data/Profile-2")
    manager = SubAppManager(test_profile)
    apps = manager.get_apps()
    print("Registered apps:", apps)
