from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel,
    QFrame, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont


class ChatHistoryWindow(QFrame):
    """
    Modern message chat window with dynamic bubble width and modern scrollbar.
    """
    MODERN_SCROLLBAR_QSS = """
        QScrollArea {
            background: transparent; 
            border: none;
        }
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 8px;
            margin: 0px 2px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #D3D3D3; /* Lighter grey handle */
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- make whole widget transparent ---
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # --- apply modern scroll area QSS ---
        self.scroll_area.setStyleSheet(self.MODERN_SCROLLBAR_QSS)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")

        self.chat_layout = QVBoxLayout(self.scroll_content)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        
        # Store message bubbles for dynamic resizing
        self.message_bubbles = [] 

    def resizeEvent(self, event):
        """Handle window resizing to update bubble maximum width."""
        super().resizeEvent(event)
        self._update_bubble_widths()

    def _update_bubble_widths(self):
        """Recalculates and sets the maximum width for all message bubbles (60%)."""
        # We use the width of the scroll area viewport for accurate 60% calculation
        if self.scroll_area.viewport().width() > 0:
            max_w = int(self.scroll_area.viewport().width() * 0.60)
            
            for bubble in self.message_bubbles:
                bubble.setMaximumWidth(max_w)
                
            # Must re-layout the container after changing size hint
            if self.scroll_content.layout():
                self.scroll_content.layout().invalidate()
            
            self.scroll_to_bottom() # Ensure position is maintained after resize

    def _create_bubble(self, text: str, bg_color: str, text_color: str) -> QLabel:
        """Helper to create and style a message bubble."""
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setFont(QFont("Segoe UI", 12))

        bubble.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: 10px;
                border-radius: 12px;
            }}
        """)
        bubble.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        
        # Initial width calculation (will be updated by resizeEvent)
        max_width = int(self.scroll_area.width() * 0.60) if self.scroll_area.width() > 0 else 400
        bubble.setMaximumWidth(max_width)
        
        self.message_bubbles.append(bubble)
        return bubble

    # ===============================================================
    # Add SENT message (blue bubble, right aligned)
    # ===============================================================
    def add_sent_message(self, text: str):
        bubble = self._create_bubble(text, "#0084FF", "white")

        holder = QHBoxLayout()
        holder.addStretch()           # push bubble to right
        holder.addWidget(bubble)
        holder.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(holder)
        self.chat_layout.addWidget(container)

        self.scroll_to_bottom()

    # ===============================================================
    # Add RECEIVED message (light bubble, left aligned)
    # ===============================================================
    def add_received_message(self, text: str):
        bubble = self._create_bubble(text, "#F1F1F1", "black")

        holder = QHBoxLayout()
        holder.addWidget(bubble)
        holder.addStretch()           # push bubble left -> right side empty
        holder.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(holder)
        self.chat_layout.addWidget(container)

        self.scroll_to_bottom()

    # ===============================================================
    # Auto scroll to bottom
    # ===============================================================
    def scroll_to_bottom(self):
        # We use a singleShot to ensure the layout has time to calculate the max height
        from PySide6.QtCore import QTimer 
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
        
# Example usage for testing (Omitted for brevity in the final application file, 
# but logic remains inside the class).