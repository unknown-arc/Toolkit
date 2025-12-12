from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QAction


class LoginViaEmail(QWidget):
    login_submitted = Signal(str, str)  # emits email and password

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login via Email")
        self.resize(900, 600)

        # --- Global Style ---
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', sans-serif;
            }

            QFrame#card {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 16px;
                padding: 40px;
            }

            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #0066ff;
            }

            QPushButton#continue {
                background-color: #000000;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#continue:hover {
                background-color: #222222;
            }
        """)

        # --- Main Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left blank section (40%)
        left_frame = QFrame()
        left_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right content section (60%)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)

        # --- Input Fields ---
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # --- Eye Icon (Show/Hide Password) ---
        self.show_password = False
        self.toggle_action = QAction(QIcon("assets/eye-off.svg"), "Show/Hide", self)
        self.toggle_action.triggered.connect(self.toggle_password_visibility)
        self.password_input.addAction(self.toggle_action, QLineEdit.TrailingPosition)

        # --- Continue Button ---
        continue_btn = QPushButton("Continue")
        continue_btn.setObjectName("continue")
        continue_btn.setFixedWidth(280)
        continue_btn.clicked.connect(self._on_continue)

        # --- Assemble card ---
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(20)
        card_layout.addWidget(continue_btn, alignment=Qt.AlignCenter)

        # --- Combine Layouts ---
        main_layout.addWidget(left_frame, stretch=2)
        main_layout.addWidget(card, stretch=3)
        self.setLayout(main_layout)

    def toggle_password_visibility(self):
        """Toggles between showing and hiding the password."""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_action.setIcon(QIcon("assets/eye.svg"))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_action.setIcon(QIcon("assets/eye-off.svg"))

    def _on_continue(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        print(f"Email: {email}, Password: {password}")
        self.login_submitted.emit(email, password)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = LoginViaEmail()
    window.show()
    sys.exit(app.exec())
