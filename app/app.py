from __future__ import annotations
import platform
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette
from pathlib import Path

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parent.parent 
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))


from  app.core.window_manager.page_manager import PageManager
from  app.core.window_manager.dialog_manager import DialogManager
from  app.core.window_manager.popup_manager import PopupManager
from  app.core.subapp_manager.subapp_manager import SubAppManager
from  app.core.lab_and_session_manager.lab_manager import LabManager
from  app.core.lab_and_session_manager.session_manager import SessionManager
from  app.core.lab_and_session_manager.registor_external_app import cleanup

class App(QMainWindow):
    def __init__(self, profile_path: Path):
        super().__init__()
        self.setWindowTitle("Toolkit App")
        self.setMinimumSize(800, 600)

        self.profile_path = profile_path
        self.subapp_manager = SubAppManager(self.profile_path)

        self.manager = PageManager()
        self.setCentralWidget(self.manager)

        self.dialog_manager = DialogManager(self)
        self.popup_manager = PopupManager(self)

        self.lab_manager = LabManager(self.profile_path)
        # self.session_manager = SessionManager()


        self.showMaximized()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = App()
#     win.show()
#     app.exec() 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1️⃣ If argument provided → use it
    if len(sys.argv) > 1:
        profile_path = Path(sys.argv[1]).resolve()

    # 2️⃣ If NO argument → use default test path
    else:
        profile_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "Profile-1"
        )
        print("⚠ No profile argument given. Using default:", profile_path)  

        # 3️⃣ Store globally if you really want
    app.profile_path = profile_path
    print("Using profile path:", app.profile_path)
    app.aboutToQuit.connect(cleanup)

    # 4️⃣ Start app
    window = App(profile_path)
    window.show()
    app.exec()      