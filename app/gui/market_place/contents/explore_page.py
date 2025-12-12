from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton
from PySide6.QtCore import Qt

class ExplorePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        header = QLabel("<h3>🔍 Explore Categories</h3>")
        header.setStyleSheet("color: #333333; margin-bottom: 20px;")
        header.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(header)
        
        grid = QGridLayout()
        categories = ["Productivity", "Graphics", "Development", "Education", "Utilities", "Games"]
        
        for i, cat in enumerate(categories):
            btn = QPushButton(f"Category: {cat}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0; 
                    border: 1px solid #cccccc;
                    border-radius: 10px; 
                    padding: 20px 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #dddddd;
                }
            """)
            grid.addWidget(btn, i // 3, i % 3) # 3 columns
            
        layout.addLayout(grid)