from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QHBoxLayout, QFrame, QSizePolicy, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QAction
from gui.widget.auth_buttons import (
    SignupButton, GuestLogin)

from gui.widget.auth_buttons import SignupButton, GuestLogin
from gui.error_widget.user_credential_failed import LoginErrorDialog
from core.event_signal import auth_sgl



class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Global Style ---
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', sans-serif;
            }

            QLabel {
                background-color: transparent;
            }

            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: #ffffff;
            }

            QLineEdit:focus {
                border: 1px solid #e0e0e0;
            }

            QFrame#line {
                background-color: #cccccc;
                height: 1px;
            }
        """)

        # --- Main layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 12, 24, 12)   # MATCH login page
        main_layout.setSpacing(12)


        # -----------------------------
        # NAME FIELD
        # -----------------------------
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFixedHeight(40)
        self.name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.name_container = QFrame()
        name_layout = QVBoxLayout(self.name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(self.name_input)

        # -----------------------------
        # EMAIL FIELD
        # -----------------------------
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFixedHeight(40)
        self.email_input.setClearButtonEnabled(True)
        self.email_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.email_container = QFrame()
        email_layout = QVBoxLayout(self.email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.addWidget(self.email_input)
        # -----------------------------
        # SIGNUP BUTTON
        # -----------------------------
        signup_btn = SignupButton()
        signup_btn.setFixedHeight(40)
        signup_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # -----------------------------
        # OR SEPARATOR
        # -----------------------------
        line = QFrame()
        line.setObjectName("line")
        line.setFixedHeight(1)

        or_label = QLabel("or")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("color: #888888; margin: 8px;")

        # -----------------------------
        # GUEST BUTTON
        # -----------------------------
        guest_btn = GuestLogin()
        guest_btn.setFixedHeight(40)
        signup_btn.setMinimumWidth(276)
        signup_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


        # Connect guest button signal
        signup_btn.clicked.connect(self.show_login_error)
        guest_btn.clicked.connect(auth_sgl.guest_log_sgl.emit)

        # Add widgets to layout
        # -----------------------------
        main_layout.addWidget(self.name_container)
        main_layout.addWidget(self.email_container)
        main_layout.addSpacing(6)
        main_layout.addWidget(signup_btn)
        main_layout.addSpacing(12)
        main_layout.addWidget(line)
        main_layout.addSpacing(-10)
        main_layout.addWidget(or_label)
        main_layout.addSpacing(-10)
        main_layout.addWidget(guest_btn)

            
    def show_login_error(self):
        dialog = LoginErrorDialog(self)
        result = dialog.exec()
        if result == QDialog.Accepted:
            print("User chose to continue as guest.")