import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PySide6.QtCore import Qt

if __name__ == '__main__':
    # Go up until we reach project root 'A'
    ROOT_DIR = Path(__file__).resolve().parent.parent
    print(ROOT_DIR)
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from quick_lab.message_input.message_input import  AdvancedMessageInputBar
from quick_lab.chat_window.chat_window import ChatHistoryWindow as ChatWindow 
from quick_lab.message_input.message_input import AdvancedMessageInputBar
from quick_lab.chat_window.chat_window import ChatHistoryWindow as ChatWindow 

try:
    from core.signal_manager import Lab_eb
except ImportError:
    class MockSignalEmitter:
        def connect(self, func): pass
        def emit(self, *args): pass
    Lab_eb = MockSignalEmitter()


class QuickLab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.is_named = False 
        self.lab_id = None 
        self.setWindowTitle("QuickLab")
        self.resize(700, 800) 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Chat History Window 
        self.chat = ChatWindow()
        layout.addWidget(self.chat, 1) 

        # 2. Container for Message Input Bar (to apply padding)
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        # 3. Message Input Bar
        self.input_bar = AdvancedMessageInputBar()
        input_layout.addWidget(self.input_bar)

        layout.addWidget(input_container)

        # Connect the send signal
        self.input_bar.on_send(self.send_message)

        # Initialize with a welcome message
        
    def send_message(self):
        msg = self.input_bar.message_input.toPlainText().strip()
        
        if msg:
            self.chat.add_sent_message(msg)

            # Clear the input (Fix for previous problem)
            self.input_bar.clear_text()
            
            # Placeholder Echo Logic (Simulate start and end)
            echo_text = "Waiting for Gemini integration..."
            self.chat.add_received_message(echo_text)
            
            # Simulate the echo end
            final_response = f"Simulated Gemini response to: '{msg[:20]}...' (Code verified.)"
           

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QuickLab()
    demo.show()
    sys.exit(app.exec())