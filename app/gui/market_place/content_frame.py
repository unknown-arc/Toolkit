# content_frame_module.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QScrollArea
from PySide6.QtCore import Qt

from .navbar import NavBar

class ContentFrame(QWidget):
    def __init__(self, nav_bar_widget, stacked_widget):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        nav_container = QWidget()
        nav_layout = QHBoxLayout(nav_container)

        nav_layout.setContentsMargins(20, 15, 20, 15) 
        
        nav_layout.addStretch(1)
        nav_layout.addWidget(nav_bar_widget) 
        nav_layout.addStretch(1)
        
        # Add the navbar container to the main layout, ensuring it stays at the top
        main_layout.addWidget(nav_container, alignment=Qt.AlignmentFlag.AlignTop)
        
        # --- 2. Main Content Area ---
        
        self.stacked_widget = stacked_widget
        
        # To ensure the content (titles/headers on the pages) starts BELOW the fixed-height 
        # nav bar, the individual page classes (HomePage, ExplorePage, etc.) 
        # must have a large TOP MARGIN applied to their internal layout. 
        # This creates the visual space below the floating nav bar.
        
        main_layout.addWidget(self.stacked_widget)
        main_layout.addStretch(1) # Ensure everything stays packed at the top