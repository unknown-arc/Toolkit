from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from gui.authentication_page.login import LoginPage
from gui.authentication_page.signup import SignupPage

from gui.frames.content_frame import ContentFrame
from gui.frames.message_frame import MessageFrame 

from gui.messages.authmessage import LoginMessage, SignupMessage

from core.event_signal import auth_sgl, page_nav_sgl



class AuthenticationManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Signup Manager")

        # --- ROOT LAYOUT ---
        self.root_layout = QHBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # Placeholder layouts (we'll add widgets dynamically)
        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.root_layout.addWidget(self.left_container)
        self.root_layout.addWidget(self.right_container)

        # Connect signals
        auth_sgl.show_login_page.connect(self.load_login_page)
        auth_sgl.show_signup_page.connect(self.load_signup_page)

        # Load default page
        self.load_login_page()

    # Clear any existing widgets in a layout
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    # ---------------------------
    # LOGIN PAGE: [Message | Content] → left: message 2, right: content 3
    # ---------------------------
    def load_login_page(self):
        self.clear_layout(self.left_layout)
        self.clear_layout(self.right_layout)

        # old_left = self.left_layout.itemAt(0).widget() if self.left_layout.count() else None
        # old_right = self.right_layout.itemAt(0).widget() if self.right_layout.count() else None

        login_page = ContentFrame(LoginPage())
        login_msg = MessageFrame(LoginMessage())

        # if old_left and old_right:
        #     slide_transition(old_left, old_right, login_msg, login_page)
        # else:
        #     # First load: no animation
        #     self.clear_layout(self.left_layout)
        #     self.clear_layout(self.right_layout)
        #     self.left_layout.addWidget(login_msg)
        #     self.right_layout.addWidget(login_page)


        login_msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        login_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets
        self.left_layout.addWidget(login_msg)
        self.right_layout.addWidget(login_page)

        # Set stretches to 2:3
        self.root_layout.setStretchFactor(self.left_container, 2)
        self.root_layout.setStretchFactor(self.right_container, 3)

    # ---------------------------
    # SIGNUP PAGE: [Content | Message] → left: content 3, right: message 2
    # ---------------------------
    def load_signup_page(self):
        self.clear_layout(self.left_layout)
        self.clear_layout(self.right_layout)

        # old_left = self.left_layout.itemAt(0).widget() if self.left_layout.count() else None
        # old_right = self.right_layout.itemAt(0).widget() if self.right_layout.count() else None

        # signup_page = ContentFrame(SignupPage())
        # signup_msg = MessageFrame(SignupMessage())

        # if old_left and old_right:
        #     slide_transition(old_left, old_right, signup_page, signup_msg)
        # else:
        #     self.clear_layout(self.left_layout)
        #     self.clear_layout(self.right_layout)
        #     self.left_layout.addWidget(signup_page)
        #     self.right_layout.addWidget(signup_msg)

        signup_page = ContentFrame(SignupPage())
        signup_msg = MessageFrame(SignupMessage())

        signup_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        signup_msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets
        self.left_layout.addWidget(signup_page)
        self.right_layout.addWidget(signup_msg)

        # Set stretches to 3:2
        self.root_layout.setStretchFactor(self.left_container, 3)
        self.root_layout.setStretchFactor(self.right_container, 2)
