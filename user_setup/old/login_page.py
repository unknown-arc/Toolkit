from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QHBoxLayout, QSizePolicy, QSpacerItem, QDialog
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon
import sys
import os
from pathlib import Path

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    print(f"ROOT_DIR set to: {ROOT_DIR}")
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from user_setup.gui.error_widget.user_credentials_failed import LoginErrorDialog
from user_setup.core.event_signal import auth_sgl as login_signal

# --- Assets ---
def icon_path(asset_name):
    base_dir = Path(__file__).parent.parent.parent
    return os.path.join(base_dir, "assets", asset_name) 

google_icon_path = icon_path("google-logo.svg")
email_icon_path = icon_path("email-logo.svg")    

class LoginPage(QWidget):
    guest_login_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - MyApp")
        self.resize(900, 600)

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

            QPushButton {
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }

            QPushButton#google {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
            }
            QPushButton#google:hover {
                background-color: #f8f8f8;
            }

            QPushButton#email {
                background-color: #0066ff;
                color: white;
                border: none;
            }
            QPushButton#email:hover {
                background-color: #1a75ff;
            }

            QPushButton#guest {
                background-color: #000000;
                color: white;
                border: none;
            }
            QPushButton#guest:hover {
                background-color: #222222;
            }

            QFrame#line {
                background-color: #cccccc;
                height: 1px;
            }

            QFrame#card {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 16px;
                padding: 40px;
            }

            QFrame#left_panel {
                background-color: #f5f5f5;
            }
        """)

        # --- Root layout (Horizontal Split) ---
        root_layout = QHBoxLayout(self)

        # ---------- Left Side (40%) ----------
        left_panel = QFrame()
        left_panel.setObjectName("left_panel")
        left_panel.setMinimumWidth(int(900 * 0.4))
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.addStretch()  # keep blank for now
        left_panel_layout.addWidget(QLabel(""), alignment=Qt.AlignCenter)
        left_panel_layout.addStretch()

        # ---------- Right Side (60%) ----------
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        # --- Title and Subtitle ---
        title = QLabel("Login and Sign-Up")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        subtitle = QLabel("For advanced use and better results")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #555555; font-size: 14px; margin-bottom: 20px;")

        # --- Alert Message ---
        alert_label = QLabel("⚠ Currently our server is not responsive, kindly continue as Guest login")
        alert_label.setAlignment(Qt.AlignCenter)
        alert_label.setStyleSheet("color: #d32f2f; font-size: 13px; font-weight: 500; margin-bottom: 10px;")
        
        '''

        # --- Button Helper Function ---
        def create_button(text, icon_path, object_name, bg_color, text_color, hover_color):
            btn = QPushButton(text)
            btn.setObjectName(object_name)
            btn.setFixedWidth(280)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setCursor(Qt.PointingHandCursor)

            btn.setStyleSheet(f"""
                QPushButton#{object_name} {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: {'1px solid #d0d0d0' if object_name == 'google' else 'none'};
                    border-radius: 8px;
                    padding: 10px 12px;
                    font-size: 16px;
                    font-weight: 500;
                    text-align: center;
                }}
                QPushButton#{object_name}:hover {{
                    background-color: {hover_color};
                }}
                QPushButton#{object_name}::menu-indicator {{
                    image: none;
                }}
            """)
            return btn


        # --- Google Button ---
        google_btn = create_button(
            "Continue with Google",
            google_icon_path,
            "google",
            "#ffffff",
            "#000000",
            "#f5f5f5"
        )

        # --- Email Button ---
        email_btn = create_button(
            "Continue with Email",
            email_icon_path,
            "email",
            "#0066ff",
            "#ffffff",
            "#1a75ff"
        )
        '''

        # --- Buttons ---
        google_btn = QPushButton("Continue with Google")
        google_btn.setObjectName("google")
        google_btn.setFixedWidth(280)
        google_btn.setIcon(QIcon(google_icon_path))
        google_btn.setIconSize(QSize(24, 24))
        google_btn.setStyleSheet("QPushButton { padding-left: 6px; }")

        email_btn = QPushButton("Continue with Email")
        email_btn.setObjectName("email")
        email_btn.setFixedWidth(280)
        email_btn.setIcon(QIcon(email_icon_path))
        email_btn.setIconSize(QSize(24, 24))
        email_btn.setStyleSheet("QPushButton { padding-left: 10px; }")

        # '''
        

        line = QFrame()
        line.setObjectName("line")
        line.setFixedHeight(1)

        or_label = QLabel("or")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("color: #888888; margin: 10px;")

        guest_btn = QPushButton("Continue as Guest")
        guest_btn.setObjectName("guest")
        guest_btn.setFixedWidth(280)
        guest_btn.clicked.connect(self._continue_as_guest)

        # --- Signals ---
        google_btn.clicked.connect(self.show_login_error)
        email_btn.clicked.connect(self.show_login_error)
        # --- Assemble Card ---
        card_layout.addSpacing(20)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(alert_label)
        card_layout.addSpacing(20)
        card_layout.addWidget(google_btn, alignment=Qt.AlignCenter)
        card_layout.addWidget(email_btn, alignment=Qt.AlignCenter)
        card_layout.addSpacing(20)
        card_layout.addWidget(line)
        card_layout.addWidget(or_label)
        card_layout.addWidget(guest_btn, alignment=Qt.AlignCenter)
        card_layout.addStretch()

        right_layout.addStretch()
        right_layout.addWidget(card, alignment=Qt.AlignCenter)
        right_layout.addStretch()

        # --- Add both sides to main layout ---
        root_layout.addWidget(left_panel, stretch=4)
        root_layout.addWidget(right_panel, stretch=6)

    def _continue_as_guest(self):
        login_signal.login_via_guest.emit()

    def show_login_error(self):
        dialog = LoginErrorDialog(self)
        result = dialog.exec()
        if result == QDialog.Accepted:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())
