import sys
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit
)
from PySide6.QtCore import Qt, QSize, QEvent # <<< ADDED QEvent
from PySide6.QtGui import QFontMetrics, QTextDocument, QIcon, QMouseEvent 

# Import the custom button classes (assuming these are available)
from quick_lab.message_input.message_composer_actions import AddFileButton, MikeButton, SendMessageButton


class AdvancedMessageInputBar(QFrame):
    """
    Advanced message input bar with event filtering to detect Enter key press.
    """
    # Configuration constants (remain the same)
    MIN_LINES = 1
    MAX_LINES = 8
    BUTTON_HEIGHT = 48 
    FRAME_VPADDING = 20
    MIN_FRAME_HEIGHT = BUTTON_HEIGHT + FRAME_VPADDING 

    MODERN_SCROLLBAR_QSS = """
        QScrollBar:vertical { border: none; background: transparent; width: 8px; margin: 0px 2px 0px 0px; }
        QScrollBar::handle:vertical { background: #B0B0B0; min-height: 20px; border-radius: 4px; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._send_callback = lambda: None 

        # 1. Outer bar styling (remains the same)
        self.setStyleSheet("""
            QFrame { background-color: white; border: 1px solid #E0E0E0; border-radius: 25px; }
        """)
        
        # Main Layout: VERTICAL
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10) 
        self.main_layout.setSpacing(4) 
        
        self._calculate_heights()

        self.setMinimumHeight(self.MIN_FRAME_HEIGHT)
        self.setMaximumHeight(self.max_frame_height) 

        # ======================================================
        # 1. AUTO-EXPANDING TEXT BOX (QTextEdit) - TOP section
        # ======================================================
        self.message_input = QTextEdit() # <<< Reverted to standard QTextEdit
        self.message_input.setPlaceholderText("Start Chat...")
        # ... (style and sizing)
        
        self.message_input.setStyleSheet(f"""
            QTextEdit {{ border: none; background-color: transparent; padding: 0px; margin: 0px; font-size: 16px; }}
            {self.MODERN_SCROLLBAR_QSS}
        """)
        
        self.message_input.setFixedHeight(self.min_text_height) 
        
        # Connect signals
        self.message_input.textChanged.connect(self.adjust_text_height)
        self.message_input.textChanged.connect(self._update_send_button_state)
        
        # --- NEW: Install event filter on the QTextEdit ---
        self.message_input.installEventFilter(self)
        # --------------------------------------------------
        
        self.main_layout.addWidget(self.message_input) 

        # ======================================================
        # 2. CONTROL BAR WIDGET - BOTTOM section (remains the same)
        # ======================================================
        self.control_bar = QWidget()
        self.control_bar.setFixedHeight(self.BUTTON_HEIGHT) 

        control_layout = QHBoxLayout(self.control_bar)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(8)

        self.add_file_btn = AddFileButton()
        control_layout.addWidget(self.add_file_btn)
        control_layout.addStretch(1) 
        self.mic_btn = MikeButton()
        control_layout.addWidget(self.mic_btn)
        self.send_button = SendMessageButton()
        self.send_button.setEnabled(False) 
        control_layout.addWidget(self.send_button)

        self.main_layout.addWidget(self.control_bar) 


    def _calculate_heights(self):
        # (remains the same)
        font_metrics = QFontMetrics(self.font())
        self.line_height = font_metrics.lineSpacing() + 10 
        self.min_text_height = self.line_height 
        self.max_text_height = self.line_height * self.MAX_LINES
        
        margins = self.main_layout.contentsMargins()
        total_v_padding = margins.top() + margins.bottom()
        
        self.max_frame_height = (self.max_text_height + 
                                 self.BUTTON_HEIGHT + 
                                 self.main_layout.spacing() + 
                                 total_v_padding)


    def _update_send_button_state(self):
        # (remains the same)
        has_text = bool(self.message_input.toPlainText().strip())
        self.send_button.setEnabled(has_text)


    def adjust_text_height(self):
        # (remains the same)
        doc: QTextDocument = self.message_input.document()
        doc.setTextWidth(self.message_input.viewport().width())
        required_height = doc.size().height() 

        new_text_height = min(required_height, self.max_text_height)
        new_text_height = max(new_text_height, self.min_text_height)

        self.message_input.setFixedHeight(new_text_height)
        
        margins = self.main_layout.contentsMargins()
        total_v_padding = margins.top() + margins.bottom()
        
        new_frame_height = (new_text_height + 
                            self.BUTTON_HEIGHT + 
                            self.main_layout.spacing() + 
                            total_v_padding)

        self.setFixedHeight(new_frame_height)
        
    # -----------------------------------------------------
    # --- NEW: EVENT FILTER METHOD TO CAPTURE KEY PRESS ---
    # -----------------------------------------------------
    def eventFilter(self, watched: QWidget, event: QEvent) -> bool:
        # 1. Check if the event is a key press on the message input widget
        if watched == self.message_input and event.type() == QEvent.KeyPress:
            key_event = event
            
            # 2. Check for Enter key press
            if key_event.key() in (Qt.Key_Return, Qt.Key_Enter):
                # 3. Check for modifier keys (Shift/Ctrl)
                if not (key_event.modifiers() & (Qt.ShiftModifier | Qt.ControlModifier)):
                    # 4. Trigger send action if button is enabled
                    if self.send_button.isEnabled():
                        self._handle_send_trigger()
                        return True  # Consume the event (stop newline creation)
        
        # For all other events, pass them along
        return super().eventFilter(watched, event)
    # -----------------------------------------------------

    # --- Public API Methods ---
    
    def _handle_send_trigger(self):
        """Called by both Enter key press (via eventFilter) and Send button click."""
        # Check performed in eventFilter for key press, but repeated here for button safety
        if self.send_button.isEnabled():
            self._send_callback()

    def get_text(self) -> str:
        return self.message_input.toPlainText().strip()

    def clear_text(self):
        self.message_input.clear()
        self.adjust_text_height() 

    def on_send(self, func):
        """Connects the external function to the internal send trigger."""
        self._send_callback = func
        
        # Connect the button click to the internal trigger
        self.send_button.clicked.connect(self._handle_send_trigger)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdvancedMessageInputBar()
    
    # Mock send function for demonstration
    def test_send():
        print(f"Message Sent: {window.get_text()}")
        window.clear_text()
        
    window.on_send(test_send)

    window.setWindowTitle("Message Input Bar Test (Event Filter)")
    window.show()
    sys.exit(app.exec())