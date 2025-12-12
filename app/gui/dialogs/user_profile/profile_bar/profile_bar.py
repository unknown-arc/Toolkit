from PySide6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QPushButton, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal

class ProfileCard(QFrame):
    """Sleek, Chrome-style clickable profile icon and name."""
    
    def __init__(self, name, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.name = name
        self.setFixedSize(120, 120)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QFrame { background: transparent; }")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Circular Icon Area
        self.icon_frame = QFrame()
        self.icon_frame.setFixedSize(60, 60)
        self.icon_frame.setStyleSheet("""
            QFrame {
                border-radius: 30px;
                background-color: #A0D2F9; /* Light blue */
                border: 2px solid transparent;
            }
            QFrame:hover {
                border: 2px solid #3498DB; /* Highlight on hover */
            }
        """)
        
        icon_layout = QVBoxLayout(self.icon_frame)
        icon_label = QLabel("👤")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 30px; color: #3498DB; padding: 0;")
        icon_layout.addWidget(icon_label)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label: Small and simple text
        name_label = QLabel(self.name.split()[0]) 
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #333; margin-top: 5px;")
        
        layout.addWidget(self.icon_frame)
        layout.addWidget(name_label)
        layout.setContentsMargins(5, 5, 5, 5)

    def mousePressEvent(self, event):
        parent_selector = self.parent().parent().parent() 
        if isinstance(parent_selector, ProfileBarWidget):
            parent_selector.profile_clicked.emit(self.data)
        super().mousePressEvent(event)


class ProfileBarWidget(QWidget):
    profile_clicked = Signal(dict) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(150)
        self.setStyleSheet("background-color: transparent;")
        
        main_layout = QHBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        # --- Center Alignment for the Profile Bar Content ---
        # 🚩 Negative point: Horizontal scroll doesn't naturally center.
        # Positive result: Using addStretch on both sides centers the profiles when they fit on one line.
        content_widget = QWidget()
        self.profile_layout = QHBoxLayout(content_widget)
        self.profile_layout.addStretch() # Left stretch for centering
        
        # --- Dummy Profile Data ---
        self.dummy_profiles = [
            {"name": "Alice Cooper", "gender": "Female", "age": "28", "email": "alice@app.com"},
            {"name": "Bob Marley", "gender": "Male", "age": "35", "email": "bob@app.com"},
            {"name": "Charlie Chaplin", "gender": "Non-binary", "age": "22", "email": "charlie@app.com"},
            {"name": "Default User", "gender": "N/A", "age": "30", "email": "default@app.com"},
        ]
        
        for profile in self.dummy_profiles:
            card = ProfileCard(profile["name"], profile)
            self.profile_layout.addWidget(card)

        # --- Add New Icon ---
        add_button = QPushButton("➕")
        add_button.setFixedSize(60, 60)
        add_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                border: 2px dashed #B3D2F9;
                border-radius: 30px;
                background-color: transparent;
                color: #B3D2F9;
                margin-top: 10px;
            }
            QPushButton:hover {
                border-color: #3498DB;
                color: #3498DB;
            }
        """)
        add_button_wrapper = QWidget()
        add_button_layout = QVBoxLayout(add_button_wrapper)
        add_button_layout.setAlignment(Qt.AlignCenter)
        add_button_layout.addWidget(add_button)
        add_button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.profile_layout.addWidget(add_button_wrapper)
        
        self.profile_layout.addStretch() # Right stretch for centering
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)