# home.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # We need a scrollable area inside the page to handle long content
        scroll_content_widget = QWidget()
        content_layout = QVBoxLayout(scroll_content_widget)
        
        # 🟢 CRITICAL FIX: Large top margin (150px) to push content down 
        # below the floating navbar area.
        content_layout.setContentsMargins(50, 150, 50, 50) 
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # --- Content Section ---
        header = QLabel("🏠 HOME: Welcome to the Marketplace!")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.setStyleSheet("font-size: 24px; color: #333;")
        content_layout.addWidget(header)
        
        # Add lots of dummy scrollable content
        for i in range(20):
             content_layout.addWidget(QLabel(f"Scrollable Content Item {i+1}"))
             
        content_layout.addStretch(1)
        
        # --- Main Layout for the Page ---
        main_page_layout = QVBoxLayout(self)
        main_page_layout.setContentsMargins(0, 0, 0, 0) # Page margins should be zero
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content_widget)
        
        main_page_layout.addWidget(scroll_area)