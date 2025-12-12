import sys
from PySide6.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from pathlib import Path

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from gui.main_window.left_panel.top_elements import TopElementWindow
from gui.main_window.left_panel.Acitivity import ActivityWidget



# Helper function to wrap a widget in a rounded container
def rounded_container(widget, radius=15, bg_color="#EDEDED", margin=10):
    """Wrap a widget inside a rounded QFrame with margin."""
    frame = QFrame()
    frame.setStyleSheet(
        f"""
        QFrame {{
            background-color: {bg_color};
            border-radius: {radius}px;
        }}
        """
    )
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(margin, margin, margin, margin)
    layout.addWidget(widget)
    return frame


class LeftPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Panel appearance
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#EDEDED"))
        # pal.setColor(QPalette.ColorRole.Window, QColor("#008000")) # Green background while working 
        self.setPalette(pal)
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)

        # Layout for the panel
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Create inner widgets
        upper = TopElementWindow()
        center = ActivityWidget()

        # Add to layout
        layout.addWidget(upper)
        layout.addWidget(center, stretch=1)  # stretch gives flexible height


        # Optional bottom spacer
        layout.addWidget(QLabel(alignment=Qt.AlignTop | Qt.AlignHCenter))


# Run standalone for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = LeftPanel()
    panel.resize(400, 700)
    panel.setWindowTitle("Left Panel")
    panel.show()
    sys.exit(app.exec())
