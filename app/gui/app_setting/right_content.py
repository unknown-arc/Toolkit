# settings_right.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsRightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(10)

        self.title = QLabel("General Settings")
        self.title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(self.title, alignment=Qt.AlignTop)

        self.content = QLabel("Here are your general preferences.")
        self.content.setFont(QFont("Segoe UI", 12))
        self.content.setWordWrap(True)
        self.layout.addWidget(self.content)

        self.layout.addStretch()

    def update_content(self, section_name: str):
        """Update the right content area based on selected section."""
        self.title.setText(f"{section_name} Settings")

        info = {
            "General": "Here you can adjust general preferences like language, theme, etc.",
            "Privacy": "Manage your privacy settings, permissions, and data options.",
            "Notifications": "Control notification types and alert preferences.",
            "Account": "Update your account information, password, and connected services."
        }
        self.content.setText(info.get(section_name, "Section not found."))
