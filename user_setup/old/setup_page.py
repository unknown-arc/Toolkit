from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QApplication
)
from PySide6.QtCore import Qt

from pathlib import Path
import sys

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

# # Import your pages
from gui.usersetup_page.setup_page1 import UserInfoForm as SetupPage1
from gui.usersetup_page.setup_page2 import OccupationSelection as SetupPage2
from gui.usersetup_page.setup_page3 import ThemeAndColorSlection as SetupPage3
# Import buttons
from gui.widget.old_button import (
    BackButton, NextButton, ContinueButton, FinishSetupButton, LaunchAppButton
)
from gui.usersetup_page.page_id import PageTracker


class SetupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)

        # === Main horizontal layout ===
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Left panel (40%) ===
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #f5f5f5;")
        main_layout.addWidget(left_panel, 2)

        # === Right panel (60%) ===
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #f5f5f5;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(24, 24, 24, 24)
        right_layout.setSpacing(0)
        main_layout.addWidget(right_panel, 3)

        # === White rounded card ===
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # === Step Tracker ===
        self.page_tracker = PageTracker(total_steps=3, current_step=1)
        card_layout.addWidget(self.page_tracker, alignment=Qt.AlignTop)

        # === Page Widgets ===
        self.pages = {
            1: SetupPage1(),
            2: SetupPage2(),
            3: SetupPage3()
        }

        for page in self.pages.values():
            page.setVisible(False)
            card_layout.addWidget(page)

        # Show the first page
        self.current_page = 1
        self.pages[self.current_page].setVisible(True)

        # === Navigation Buttons ===
        self.nav_layout = QHBoxLayout()
        card_layout.addLayout(self.nav_layout)
        self._add_navigation_buttons()

        # Add card to right panel
        right_layout.addWidget(card)

    def _add_navigation_buttons(self):
        # Clear previous buttons
        for i in reversed(range(self.nav_layout.count())):
            widget = self.nav_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Depending on current page, add buttons
        if self.current_page == 1:
            self.continue_btn = ContinueButton()
            self.nav_layout.addStretch()
            self.nav_layout.addWidget(self.continue_btn)

            self.continue_btn.continue_signal.connect(lambda: self.show_page(2))

        elif self.current_page == 2:
            self.back_btn = BackButton()
            self.continue_btn = ContinueButton()
            self.nav_layout.addWidget(self.back_btn)
            self.nav_layout.addStretch()
            self.nav_layout.addWidget(self.continue_btn)

            self.back_btn.back_signal.connect(lambda: self.show_page(1))
            self.continue_btn.continue_signal.connect(lambda: self.show_page(3))

        elif self.current_page == 3:
            self.back_btn = BackButton()
            self.finish_btn = FinishSetupButton()
            self.launch_btn = LaunchAppButton()
            self.nav_layout.addWidget(self.back_btn)
            self.nav_layout.addStretch()
            self.nav_layout.addWidget(self.finish_btn)
            self.nav_layout.addWidget(self.launch_btn)

            self.back_btn.back_signal.connect(lambda: self.show_page(2))
            self.finish_btn.finish_signal.connect(self.finish_setup)
            self.launch_btn.launch_signal.connect(self.launch_app)

    def show_page(self, page_id):
        # Hide current page
        self.pages[self.current_page].setVisible(False)

        # Update completed steps
        completed = list(range(1, page_id))
        self.page_tracker.set_completed_steps(completed)

        # Show new page
        self.current_page = page_id
        self.pages[self.current_page].setVisible(True)

        # Update step tracker
        self.page_tracker.set_current_step(self.current_page)

        # Update navigation buttons
        self._add_navigation_buttons()

    def finish_setup(self):
        print("Finish Setup clicked!")

    def launch_app(self):
        print("Launch App clicked!")


# --- Preview ---
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SetupPage()
    window.show()
    sys.exit(app.exec())
