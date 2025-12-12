from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from core.event_signal import auth_sgl


class LoginErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.setFixedSize(400, 180)

        # --- Matching Styles ---
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
            }

            QLabel {
                background-color: transparent;
                color: #d32f2f;
                font-size: 15px;
                font-weight: 600;
            }

            QPushButton {
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                background-color: #000000;
                color: white;
                border: none;
            }

            QPushButton:hover {
                background-color: #222222;
            }
        """)

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # --- Text ---
        label = QLabel("⚠ Unable to log-in or sign-up")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        # --- Guest Button (matching main Guest button) ---
        guest_button = QPushButton("Continue as Guest")
        guest_button.setFixedWidth(280)   # same width as main page
        guest_button.clicked.connect(self.on_guest_clicked)

        # --- Assemble Layout ---
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(guest_button, alignment=Qt.AlignCenter)
        layout.addStretch()

    def on_guest_clicked(self, checked=False):
        auth_sgl.guest_log_sgl.emit()
        self.accept()   

# guest_button.clicked.connect(on_guest_clicked)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    dialog = LoginErrorDialog()
    dialog.show()

    app.exec()