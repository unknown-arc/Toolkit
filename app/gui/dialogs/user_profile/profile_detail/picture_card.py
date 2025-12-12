from PySide6.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt

class PictureCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300) # Defined size for left card
        
        # Outer card styling
        self.setStyleSheet("""
            QFrame {
                background-color: #3498DB; /* Strong blue background */
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
                border: none;
            }
        """)
        
        v_layout = QVBoxLayout(self)
        v_layout.setAlignment(Qt.AlignCenter)
        v_layout.setSpacing(20)

        # Circular Icon Area
        self.circular_frame = QFrame()
        self.circular_frame.setFixedSize(160, 160)
        self.circular_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 80px;
                border: 5px solid #2980B9; /* Darker blue border */
            }
        """)
        
        circular_layout = QVBoxLayout(self.circular_frame)
        self.proto_icon = QLabel("👤")
        self.proto_icon.setAlignment(Qt.AlignCenter)
        self.proto_icon.setStyleSheet("font-size: 80px; color: #2C3E50;")
        circular_layout.addWidget(self.proto_icon)
        circular_layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_label = QLabel("Loading Name...")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;") # High contrast text
        
        v_layout.addWidget(self.circular_frame)
        v_layout.addWidget(self.name_label)
        
    def set_name(self, name):
        self.name_label.setText(name)