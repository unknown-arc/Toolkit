from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

class AppsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        header = QLabel("<h3>✨ Featured Apps</h3>")
        header.setStyleSheet("color: #333333; margin-bottom: 10px;")
        header.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(header)

        app_list = QListWidget()
        app_list.setStyleSheet("""
            QListWidget { border: none; }
            QListWidget::item { padding: 10px; margin: 5px 0; border-radius: 8px; }
            QListWidget::item:hover { background: #e8f5e9; }
        """)
        
        for i in range(15):
            item = QListWidgetItem(f"App Showcase #{i+1} - Editor/Tool")
            app_list.addItem(item)
            
        layout.addWidget(app_list)