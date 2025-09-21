from PySide6.QtWidgets import QApplication, QFileDialog
import sys

def select_directory():
    app = QApplication.instance() or QApplication(sys.argv)
    folder = QFileDialog.getExistingDirectory(None, "Select Download Folder")
    return folder


