# login_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QDialog,
    QPushButton, QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QIcon, QAction

from core.login_validator import Validator
from core.event_signal import auth_sgl

# Replace with your imports for custom widgets/icons
from gui.widget.auth_buttons import (
    LoginButton, AppleIcon, GoogleIcon,
    GitHubIcon, OutlookIcon
)
from gui.animation.error_shake import shake_widget
from gui.error_widget.user_credential_failed import LoginErrorDialog

class LoginPage(QWidget):
    login_submitted = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Keep running animations so they don't get GC'd
        self._anims = []

        # Basic stylesheet (inputs + error)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                font-family: "Segoe UI", sans-serif;
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
            QLineEdit[invalid="true"] {
                border: 2px solid #ff3333;
            }
            QLabel#error {
                color: #ff3333;
                font-size: 13px;
            }

            QLabel#forgot {
                color: #0066ff;
                background: transparent; /* ensure transparent bg */
            }
            QLabel#forgot:hover {
                text-decoration: underline;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 12, 24, 12)
        main_layout.setSpacing(12)

        # ------------ Email (wrapped in a container to allow shaking) ------------
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setClearButtonEnabled(True)
        self.email_input.setFixedHeight(40)
        self.email_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.email_container = QFrame()
        email_container_layout = QVBoxLayout(self.email_container)
        email_container_layout.setContentsMargins(0, 0, 0, 0)
        email_container_layout.addWidget(self.email_input)

        self.email_input.installEventFilter(self)
        self.email_input.textChanged.connect(self._reset_email_style)
        

        # ------------ Password (wrapped in container) ------------
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.password_container = QFrame()
        password_container_layout = QVBoxLayout(self.password_container)
        password_container_layout.setContentsMargins(0, 0, 0, 0)

        self.password_input.installEventFilter(self)
        self.password_input.textChanged.connect(self._reset_password_style)

        # Password eye toggle
        self.show_password = False
        self.toggle_action = QAction(QIcon("assets/eye-off.svg"), "Toggle", self)
        self.toggle_action.triggered.connect(self.toggle_password)
        self.password_input.addAction(self.toggle_action, QLineEdit.TrailingPosition)

        password_container_layout.addWidget(self.password_input)

        # ------------ Error Label (hidden by default) ------------
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setWordWrap(True)
        self.error_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.error_label.hide()  # hidden initially

        # ------------ Forgot label (right aligned) ------------
        self.forgot_label = QLabel("Forgot Password?")
        self.forgot_label.setObjectName("forgot")
        self.forgot_label.setAlignment(Qt.AlignRight)
        self.forgot_label.setCursor(Qt.PointingHandCursor)
        # Make background transparent explicitly (helps if parent frames had background)
        self.forgot_label.setStyleSheet("background: transparent;")

        # ------------ Login Button ------------
        self.login_btn = LoginButton()
        # same height as inputs, expand horizontally but min width 200
        self.login_btn.setFixedHeight(40)
        self.login_btn.setMinimumWidth(200)
        self.login_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_btn.clicked.connect(self._on_continue)

        # ------------ Social icons and separator ------------
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background: #e0e0e0;")


        self.google_icon = GoogleIcon()
        self.apple_icon = AppleIcon()
        self.github_icon = GitHubIcon()
        self.outlook_icon = OutlookIcon()
        
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(6)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(self.google_icon)
        icon_layout.addWidget(self.apple_icon)
        icon_layout.addWidget(self.github_icon)
        icon_layout.addWidget(self.outlook_icon)

        # ------------ connect signals ------------
        self.forgot_label.mousePressEvent = lambda event:self.show_login_error()
        self.google_icon.clicked.connect(self.show_login_error)
        self.apple_icon.clicked.connect(self.show_login_error)
        self.github_icon.clicked.connect(self.show_login_error)
        self.outlook_icon.clicked.connect(self.show_login_error)       

        # ---------- assemble layout ----------
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.email_container)
        main_layout.addWidget(self.password_container)
        main_layout.addWidget(self.forgot_label)
        main_layout.addSpacing(6)
        # Add button full width (no alignment center)
        main_layout.addWidget(self.login_btn)
        main_layout.addSpacing(12)
        main_layout.addWidget(line)
        main_layout.addLayout(icon_layout) 


    def show_login_error(self):
        dialog = LoginErrorDialog(self)
        result = dialog.exec()
        # if result == QDialog.Accepted:
        #     auth_sgl.guest_log_sgl.emit
        #     print("Continuing as Guest...")
            


    # ----------------------------
    # password toggle
    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_action.setIcon(QIcon("assets/eye.svg"))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_action.setIcon(QIcon("assets/eye-off.svg"))

    # ----------------------------
    # show error (text + red border + shake)
    def _show_error(self, email_bad=False, password_bad=False,
                message="Please enter valid email and password"):
    # Show text
        self.error_label.setText(message)
        self.error_label.show()

        # Mark fields invalid via property (do NOT call setStyleSheet here)
        if email_bad:
            self.email_input.setProperty("invalid", True)
            # repolish to apply the property style immediately
            self.email_input.style().unpolish(self.email_input)
            self.email_input.style().polish(self.email_input)
            # shake container
            anim = shake_widget(self.email_container, distance=8, duration=300)
            if anim:
                self._anims.append(anim)
        else:
            # ensure property is cleared
            self.email_input.setProperty("invalid", False)
            self.email_input.style().unpolish(self.email_input)
            self.email_input.style().polish(self.email_input)

        if password_bad:
            self.password_input.setProperty("invalid", True)
            self.password_input.style().unpolish(self.password_input)
            self.password_input.style().polish(self.password_input)
            anim = shake_widget(self.password_container, distance=8, duration=300)
            if anim:
                self._anims.append(anim)
        else:
            self.password_input.setProperty("invalid", False)
            self.password_input.style().unpolish(self.password_input)
            self.password_input.style().polish(self.password_input)


    def _clear_error_states(self):
        # hide label and clear invalid property for both inputs
        self.error_label.hide()

        self.email_input.setProperty("invalid", False)
        self.email_input.style().unpolish(self.email_input)
        self.email_input.style().polish(self.email_input)

        self.password_input.setProperty("invalid", False)
        self.password_input.style().unpolish(self.password_input)
        self.password_input.style().polish(self.password_input)


    def _reset_email_style(self):
        # called on textChanged and FocusIn
        if self.email_input.property("invalid"):
            self.email_input.setProperty("invalid", False)
            self.email_input.style().unpolish(self.email_input)
            self.email_input.style().polish(self.email_input)
        self.error_label.hide()


    def _reset_password_style(self):
        if self.password_input.property("invalid"):
            self.password_input.setProperty("invalid", False)
            self.password_input.style().unpolish(self.password_input)
            self.password_input.style().polish(self.password_input)
        self.error_label.hide()


    def eventFilter(self, obj, event):
        # watch for focus in on inputs
        if obj == self.email_input and event.type() == QEvent.FocusIn:
            self._reset_email_style()
        elif obj == self.password_input and event.type() == QEvent.FocusIn:
            self._reset_password_style()
        return super().eventFilter(obj, event)




    # ----------------------------
    # click handler
    def _on_continue(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        email_ok = Validator.is_valid_email(email)
        pass_ok = Validator.is_valid_password(password)

        # reset visuals
        self._clear_error_states()

        if not email_ok or not pass_ok:
            # show appropriate error
            self._show_error(email_bad=not email_ok, password_bad=not pass_ok,
                             message="Please enter valid email and password")
            return

        self.show_login_error()    

        # success clear error and emit
        # self._clear_error_states()
        # self.login_submitted.emit(email, password)

  

