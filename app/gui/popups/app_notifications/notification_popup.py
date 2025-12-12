from PySide6.QtWidgets import QDialog, QVBoxLayout, QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor

from gui.popups.app_notifications.notifications import NotificationsWidget # Import the content widget

class NotificationPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 1. Reduce Height (Approx. 15% reduction from 400px to 340px)
        self.setFixedSize(300, 340) 
        
        # Popup behavior: auto-close when clicking outside
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        
        # 2. Rounded Popup Styling
        # 🚩 Negative point: Shadow simulation requires QDialog to be solid.
        # Positive result: Provides a professional, floating card look.
        self.setStyleSheet("""
            NotificationPopup {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px; /* Rounded corners on the whole popup */
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
        """)

        # --- Content Layout ---
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(0)
        
        # --- Header ---
        # We need a Header, but without the bell icon (Requested)
        header = QLabel("Notifications")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2C3E50;
                padding: 10px 0;
                border-bottom: 1px solid #F0F0F0;
            }
        """)

        # --- Content ---
        self.notifications_widget = NotificationsWidget()
        
        # --- Assembly ---
        v_layout.addWidget(header)
        v_layout.addWidget(self.notifications_widget)
        
        # Reduce margins for a more compact, professional look
        v_layout.setContentsMargins(0, 0, 0, 0) 


    def show_below(self, button, alignment="right"):
        """
        Position the popup just below the button, aligned to the right by default.
        """
        
        btn_pos = button.mapToGlobal(QPoint(0, button.height()))
        x = btn_pos.x()

        if alignment == "center":
            x = btn_pos.x() + (button.width() // 2) - (self.width() // 2)
        elif alignment == "right":
            # Align the right edge of the popup with the right edge of the button
            x = btn_pos.x() + button.width() - self.width()

        # Simple bounds check
        screen_width = QApplication.primaryScreen().geometry().width()
        if x + self.width() > screen_width:
            x = screen_width - self.width() - 10 
        
        self.move(x, btn_pos.y() + 5) 
        self.show()

# --- Example Usage ---
if __name__ == "__main__": 
    from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget
    import sys

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Main App Window")
            self.setGeometry(100, 100, 800, 600)
            
            central_widget = QWidget()
            main_layout = QVBoxLayout(central_widget)
            
            self.notif_button = QPushButton("Open Notifications")
            self.notif_button.setFixedSize(150, 40)
            self.notif_button.clicked.connect(self.show_notification_popup)

            main_layout.addStretch()
            main_layout.addWidget(self.notif_button, alignment=Qt.AlignCenter)
            main_layout.addStretch()
            
            self.setCentralWidget(central_widget)

        def show_notification_popup(self):
            # Pass 'self' (the main window) as the parent
            self.popup = NotificationPopup(self)
            self.popup.show_below(self.notif_button, alignment="right")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())