from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QCursor


class ContinueButton(QPushButton):
    """Outlined Continue button that fills and adds arrow on hover."""

    continue_signal = Signal()  

    def __init__(self, text="Continue", parent=None):
        super().__init__(text, parent)
        self.default_text = text
        self.hover_text = f"{text} →"  # Text to show on hover

        self.setFixedSize(180, 40)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
        """)

        # Enable hover events
        self.setMouseTracking(True)
        self.installEventFilter(self)

        # Connect the normal clicked signal to our custom signal
        self.clicked.connect(self.continue_signal.emit)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            self.setText(self.hover_text)
        elif event.type() == QEvent.Leave:
            self.setText(self.default_text)
        return super().eventFilter(source, event)


class BackButton(QPushButton):
    """Circular back button with arrow symbol."""

    back_signal = Signal()  

    def __init__(self, parent=None):
        super().__init__("←", parent)  # just the arrow symbol

        self.setFixedSize(42, 42)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 4px solid #000000;
                border-radius: 21px;  /* half of size for perfect circle */
                font-size: 28px;
                font-weight: 1000;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
        """)

        # Connect the normal clicked signal to our custom signal
        self.clicked.connect(self.back_signal.emit)    

class NextButton(QPushButton):
    """Circular back button with arrow symbol."""

    next_signal = Signal()  

    def __init__(self, parent=None):
        super().__init__("→", parent)  # just the arrow symbol

        self.setFixedSize(42, 42)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 4px solid #000000;
                border-radius: 21px;  /* half of size for perfect circle */
                font-size: 28px;
                font-weight: 1000;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
        """)

        self.clicked.connect(self.next_signal.emit)    

class FinishSetupButton(QPushButton):
    """Hollow 'Finish Setup' button that adds arrow on hover but keeps color same."""

    finish_signal = Signal()

    def __init__(self, text="Finish Setup", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(180, 40)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Fixed hollow style (no color change on hover)
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }
        """)

        self.clicked.connect(self.finish_signal.emit)   



class LaunchAppButton(QPushButton):
    """Solid black button to launch the app."""

    launch_signal = Signal()

    def __init__(self, text="Launch App", parent=None):
        super().__init__(text, parent)
        self.default_text = text
        self.hover_text = f"{text} →"  # text changes only
        self.setFixedSize(180, 40)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #111111;  /* slight hover darken */
            }
        """)

        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.clicked.connect(self.launch_signal.emit)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            self.setText(self.hover_text)
        elif event.type() == QEvent.Leave:
            self.setText(self.default_text)
        return super().eventFilter(source, event)    


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout(window)

    back_btn = BackButton()
    next_btn = NextButton()
    continue_btn = ContinueButton()
    finish_btn = FinishSetupButton()
    launch_btn = LaunchAppButton()

    layout.addWidget(back_btn)
    layout.addWidget(next_btn)
    layout.addWidget(continue_btn)
    layout.addWidget(finish_btn)    
    layout.addWidget(launch_btn)

    window.show()
    app.exec()