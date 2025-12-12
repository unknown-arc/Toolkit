from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt

# Import the cards
from .picture_card import PictureCard
from .details_card import DetailsCard

class ProfileDetailWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 🚩 Center Alignment Logic for the Cards
        # We use a master QVBoxLayout to hold the content centered vertically,
        # and an inner QHBoxLayout to arrange the cards horizontally.
        master_layout = QVBoxLayout(self)
        master_layout.setAlignment(Qt.AlignCenter) # Center content block vertically
        
        h_layout = QHBoxLayout()
        h_layout.setSpacing(25) # Spacing between cards
        
        self.picture_card = PictureCard()
        self.details_card = DetailsCard()
        
        # Set fixed size ratio for the cards
        self.details_card.setMinimumWidth(550)
        self.details_card.setFixedHeight(300)

        h_layout.addWidget(self.picture_card)
        h_layout.addWidget(self.details_card)
        
        # Create a container widget for the HBox so it can be centered
        content_wrapper = QWidget()
        content_wrapper.setLayout(h_layout)
        
        master_layout.addWidget(content_wrapper)
        
    def update_details(self, data):
        """Passes update data to both picture and detail cards."""
        self.picture_card.set_name(data.get("name", "Unknown User"))
        self.details_card.update_values(data)