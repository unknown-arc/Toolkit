from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWidgets import QApplication

from core.auth_manager import AuthenticationManager
from core.setup_manager import UserSetupManager
# 
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main App Window")

        root = QWidget() 
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        # Create the Authentication Manager
        self.auth_manager = AuthenticationManager()
        layout.addWidget(self.auth_manager)

        # self.setup_manager = UserSetupManager()
        # layout.addWidget(self.setup_manager)

        # self.load_setup_manager()

        # self.term_and_condition = pass
        # layout.addWidget(self.term_and_condition)


    # def load_setup_manager(self):
    #     self.setup_manager = UserSetupManager()
    #     layout.addWidget(self.setup_manager)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 500)
    window.show()

    sys.exit(app.exec())
