from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class NotificationsWidget(QWidget):
    """
    The content area for notifications, designed to be vertically centered 
    with a clear "no notifications" message.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- Layout for Content ---
        main_layout = QVBoxLayout(self)
        
        # 🚩 Negative point: Using QWidget as a wrapper requires manual styling.
        # This gives the positive control to ensure rounded corners on the content area.
        self.setStyleSheet("""
            QWidget {
                background-color: transparent; /* Keep background transparent to see parent's style */
                border-radius: 6px; /* Ensure content container is rounded */
            }
        """)
        
        # --- Empty State Label ---
        self.empty_label = QLabel("No new notifications")
        self.empty_label.setAlignment(Qt.AlignCenter)
        
        # Simple, readable text styling
        self.empty_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #7F8C8D; /* Subtle grey */
                padding: 50px 0; /* Add vertical padding for height/centering */
            }
        """)
        
        # --- Assembly ---
        # Add a stretch before and after the label to center it vertically
        main_layout.addStretch()
        main_layout.addWidget(self.empty_label)
        main_layout.addStretch()
        
        # Set content margins to zero to maximize the inner space
        main_layout.setContentsMargins(10, 10, 10, 10)