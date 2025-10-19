import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QRect
from central_panel.Quick_lab import QuickLabWidget

# QuickLabWidget definition (like before)
class CenterPanel(QWidget):
    """Standalone central panel demo with QuickLabWidget centered and flexible."""

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

        # Create QuickLabWidget
        self.quick_lab = QuickLabWidget(self)

    def resizeEvent(self, event):
        """Resize QuickLabWidget proportionally and center it."""
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

        # Center the QuickLabWidget
        x = (self.width() - width) / 2
        y = (self.height() - height) / 2
        self.quick_lab.setGeometry(QRect(int(x), int(y), int(width), int(height)))

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CenterPanel()
    demo.show()
    sys.exit(app.exec())