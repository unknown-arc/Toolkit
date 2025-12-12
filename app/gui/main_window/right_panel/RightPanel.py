from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette
from pathlib import Path
import sys

if __name__ == "__main__":
    # Go up until we reach project root 'A'
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from core.signal_manager import Quickaccess_eb
from gui.main_window.right_panel.app_quickaccess_drawel import IconPanel
from gui.main_window.right_panel.app_quickaccess_icon import QuickAppEdit

class RightPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#EDEDED"))
        # pal.setColor(QPalette.ColorRole.Window, QColor("#008000")) # Green background while working
        self.setPalette(pal)
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setStyleSheet("color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.quickaccessedit_button = QuickAppEdit()
        self.quickaccessedit_button.clicked.connect(Quickaccess_eb.open_quickaccess_dialog.emit)

        self.quickaccess_drawel = IconPanel()

        layout.addWidget(self.quickaccess_drawel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)
        layout.addWidget(self.quickaccessedit_button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)



        # layout.addWidget(QLabel(alignment=Qt.AlignTop | Qt.AlignHCenter))
