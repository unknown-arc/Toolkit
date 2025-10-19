import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QHBoxLayout
)

class SetupWindow(QWidget):
    """A GUI window for the initial application setup."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initial Setup")
        self.setMinimumWidth(400)
        self.config_data = None
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface of the window."""
        layout = QVBoxLayout(self)

        # Instruction Label
        info_label = QLabel("Please configure the application before first use.")
        layout.addWidget(info_label)

        # --- Download Location Input ---
        download_label = QLabel("Preferred Download Location:")
        layout.addWidget(download_label)
        
        # Layout for the text box and browse button
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("e.g., C:/Users/YourUser/Downloads")
        path_layout.addWidget(self.path_edit)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_folder)
        path_layout.addWidget(browse_button)
        
        layout.addLayout(path_layout)
        
        # --- Save Button ---
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_and_close)
        layout.addWidget(save_button)

    def browse_folder(self):
        """Opens a dialog to let the user select a folder."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            os.path.expanduser("~") # Start in the user's home directory
        )
        if directory:
            self.path_edit.setText(directory)

    def save_and_close(self):
        """Saves the entered data and closes the window."""
        download_location = self.path_edit.text()
        
        if not download_location:
            # You could add a pop-up here for a better user experience,
            # but for simplicity, we'll just print to the console.
            print("⚠️ Download location cannot be empty.")
            return

        # This dictionary structure matches the one in config_handler.py
        self.config_data = {
            "download_location": download_location,
            "default_quality": "best"
        }
        self.close()

def run_gui_setup():
    """
    Creates and runs the PySide6 setup application.
    
    Returns:
        dict: The configuration data entered by the user.
    """
    app = QApplication.instance() or QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    app.exec() # This starts the event loop and blocks until the window is closed.
    return window.config_data

if __name__ == '__main__':
    # This allows you to test the GUI independently
    config = run_gui_setup()
    print("Configuration received from GUI:", config)
