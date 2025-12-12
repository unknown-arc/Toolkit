from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor

# Import Components from the new structure
from .profile_bar.profile_bar import ProfileBarWidget
from .profile_detail.profile_details import ProfileDetailWidget

class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 🚩 Setup for Modal Overlay
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        if parent:
            self.setGeometry(parent.geometry())
        else:
            self.resize(1200, 800)

        # Create the MAIN Content container to hold all UI elements
        self.content_container = QWidget(self)
        self.content_container.setObjectName("ContentContainer")
        # Define fixed size for a clean modal window
        self.content_container.setFixedSize(1000, 700) 

        # Main Vertical Layout for the Content Container
        v_layout = QVBoxLayout(self.content_container)

        # --- Top Bar (Close Button) ---
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_button = QPushButton("✖")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.accept)
        top_bar.addWidget(close_button)

        # --- Custom Widgets ---
        self.profile_bar = ProfileBarWidget()
        self.detail_area = ProfileDetailWidget()

        # --- Connection Logic (Dummy Data) ---
        if self.profile_bar.dummy_profiles:
            initial_data = self.profile_bar.dummy_profiles[0]
            self.detail_area.update_details(initial_data)
        
        # Connect the selector signal to the detail widget update method
        self.profile_bar.profile_clicked.connect(self.detail_area.update_details)

        # --- Assembly ---
        v_layout.addLayout(top_bar)
        v_layout.addWidget(QLabel("User Management Console"), alignment=Qt.AlignCenter)
        v_layout.addWidget(self.profile_bar)
        v_layout.addWidget(self.detail_area)
        v_layout.addStretch()
        
        v_layout.setContentsMargins(20, 10, 20, 20)
        
        # Style for the professional container
        self.setStyleSheet("""
            QWidget#ContentContainer {
                background-color: white;
                border-radius: 18px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50; /* Dark, professional color */
                padding: 10px 0;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
                color: #A0A0A0;
            }
            QPushButton:hover {
                color: #E74C3C; /* Red on hover */
            }
        """)

        # Center the content container
        self.center_content()

    def center_content(self):
        parent_size = self.size()
        container_size = self.content_container.size()
        self.content_container.move(
            (parent_size.width() - container_size.width()) // 2,
            (parent_size.height() - container_size.height()) // 2
        )

    # Dimming effect
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150)) 
        super().paintEvent(event)

if __name__ == "__main__": 
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dlg = UserProfileDialog()
    dlg.exec()