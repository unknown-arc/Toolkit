from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from core.event_signal import auth_sgl

class LoginMessage(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Welcome Back! Please login."))

        btn = QPushButton("Create new account")
        btn.clicked.connect(auth_sgl.show_signup_page.emit)
        layout.addWidget(btn)

class SignupMessage(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Create Your Account"))

        btn = QPushButton("Already have an account? Login")
        btn.clicked.connect(auth_sgl.show_login_page.emit)
        layout.addWidget(btn)