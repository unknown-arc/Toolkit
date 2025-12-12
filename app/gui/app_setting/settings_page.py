# main_settings_page.py
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from pathlib import Path
import sys

if __name__ == "__main__":
    # Go up until we reach project root 'A'
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from gui.app_setting.left_content import SettingsLeftPanel
from gui.app_setting.right_content import SettingsRightPanel


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Settings Page")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.resize(1000, 700)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left panel
        self.left = QFrame()
        self.left.setStyleSheet("background-color: #fafafa; border-right: 1px solid #e0e0e0;")
        left_layout = QHBoxLayout(self.left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_panel = SettingsLeftPanel()
        left_layout.addWidget(self.left_panel)

        # Right panel
        self.right = QFrame()
        self.right.setStyleSheet("background-color: #ffffff;")
        right_layout = QHBoxLayout(self.right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_panel = SettingsRightPanel()
        right_layout.addWidget(self.right_panel)

        layout.addWidget(self.left, 1)
        layout.addWidget(self.right, 5)

        # Connect left menu clicks to right panel updates
        self.left_panel.section_selected.connect(self.right_panel.update_content)


# --- Preview ---
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SettingsPage()
    window.showMaximized()
    sys.exit(app.exec())
