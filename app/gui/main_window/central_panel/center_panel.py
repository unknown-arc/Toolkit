import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QRect

from pathlib import Path

if __name__ == "__main__":
    # Go up until we reach project root 'A'
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from core.lab_and_session_manager.session_manager import SessionManager

# LabWindow definition (like before)
class CenterPanel(QWidget):
    """Standalone central panel demo with LabWindow centered and flexible."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Central Panel Demo")
        self.resize(1200, 900)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#EDEDED"))
        self.setPalette(palette)

        # Layout for the central panel (just for consistent margins)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Create LabWindow
        self.quick_lab = SessionManager(self)

    def resizeEvent(self, event):
        """Resize LabWindow proportionally and center it."""
        panel_width = self.width() - 20  # consider layout margins
        panel_height = self.height() - 20

        # Compute 10:9 ratio
        ratio_width = panel_height * 10 / 9
        ratio_height = panel_width * 9 / 10

        if ratio_width <= panel_width:
            width = ratio_width
            height = panel_height
        else:
            width = panel_width
            height = ratio_height

        # Enforce minimum size
        width = max(width, 600)
        height = max(height, 500)

        # Center the LabWindow
        x = (self.width() - width) / 2
        y = (self.height() - height) / 2
        self.quick_lab.setGeometry(QRect(int(x), int(y), int(width), int(height)))

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CenterPanel()
    demo.show()
    sys.exit(app.exec())