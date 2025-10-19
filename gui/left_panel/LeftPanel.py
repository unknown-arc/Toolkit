import sys
from PySide6.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

# Import your custom widgets
from left_panel.upper import HelloWidget
from left_panel.clock import DigitalClock
from left_panel.Acitivity import ActivityWidget


# Helper function to wrap a widget in a rounded container
def rounded_container(widget, radius=15, bg_color="#FFFFFF", margin=10):
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
        self.setPalette(pal)
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)

        # Layout for the panel
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Create inner widgets
        upper = HelloWidget()
        activity = ActivityWidget()
        digital = DigitalClock()

        # Wrap them
        upper_frame = rounded_container(upper)
        activity_frame = rounded_container(activity)
        digital_frame = rounded_container(digital)

        # Make Activity flexible (expand vertically)
        activity_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add to layout
        layout.addWidget(upper_frame)
        layout.addWidget(activity_frame, stretch=1)  # stretch gives flexible height
        layout.addWidget(digital_frame)

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
