# app/gui/widget/icon_panel.py
from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from pathlib import Path
import json
import sys

# Make sure your signal manager is imported correctly
from core.signal_manager import Lab_eb


def load_icons():
    """Load apps.json directly from the global profile path stored in QApplication."""
    app = QApplication.instance()
    profile_path = getattr(app, "profile_path", None)
    if not profile_path or not Path(profile_path).exists():
        print("[IconPanel] Profile path invalid:", profile_path)
        return []

    apps_file = Path(profile_path) / "data" / "json_data" / "subapps.json"
    if not apps_file.exists():
        print("[IconPanel] apps.json not found at:", apps_file)
        return []

    try:
        data = json.loads(apps_file.read_text(encoding="utf-8"))
    except Exception as e:
        print("[IconPanel] Failed to load apps.json:", e)
        return []

    # apps.json can be a dict of apps
    if isinstance(data, dict):
        entries = list(data.values())
    elif isinstance(data, list):
        entries = data
    else:
        print("[IconPanel] apps.json has unexpected format")
        return []

    icon_list = []
    for item in entries:
        # Only keep entries that have id, name, and icon
        if all(k in item for k in ("id", "name", "icon")):
            icon_path = Path(item["icon"].replace("\\", "/")).resolve()
            if icon_path.exists():
                icon_list.append({
                    "id": item["id"],
                    "name": item["name"],
                    "icon": icon_path
                })
            else:
                print(f"[IconPanel] Icon file not found for {item['name']}: {icon_path}")
    return icon_list


class IconButton(QPushButton):
    """Button for a single app icon."""
    def __init__(self, icon_path, icon_name, icon_id, parent=None):
        super().__init__(parent)
        self.icon_id = icon_id

        self.default_icon_size = 24
        self.hover_icon_size = 36

        self.setFixedSize(48, 48)
        self.setIconSize(QSize(self.default_icon_size, self.default_icon_size))
        self.setIcon(QIcon(str(icon_path)))
        self.setToolTip(icon_name)
        self.setFlat(True)

        # Styles
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border-radius: 24px;
                padding: 6px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.5);
            }
        """)

        # Emit signal on click
        self.clicked.connect(lambda: Lab_eb.add_lab.emit(self.icon_id))

    def enterEvent(self, event):
        self.setIconSize(QSize(self.hover_icon_size, self.hover_icon_size))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIconSize(QSize(self.default_icon_size, self.default_icon_size))
        super().leaveEvent(event)


class IconPanel(QWidget):
    """Vertical panel that displays all app icons."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        ICON_DATA = load_icons()
        if not ICON_DATA:
            print("[IconPanel] No icons loaded")

        for item in ICON_DATA:
            btn = IconButton(
                icon_path=item["icon"],
                icon_name=item["name"],
                icon_id=item["id"]
            )
            layout.addWidget(btn)


if __name__ == "__main__":
    # Test run
    ROOT_DIR = Path(__file__).resolve().parents[4]  # <-- correct project root
    PROFILE = ROOT_DIR / "user_data" / "Profile-2"

    app = QApplication(sys.argv)
    app.profile_path = PROFILE

    window = IconPanel()
    window.show()
    sys.exit(app.exec())
