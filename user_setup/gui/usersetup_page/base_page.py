from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from gui.messages.authmessage import LoginMessage, SignupMessage
from gui.messages.setupmessage import FormMessage, OccupationMessage, AppearanceMessage
from gui.animation.auth_slide import slide_transition

from core.event_signal import page_nav_sgl
from gui.widget.navigation_bar import NavigationBar
from gui.frames.content_frame import ContentFrame
from gui.frames.message_frame import MessageFrame

from gui.usersetup_page.us_pg1 import UserInfoForm as SetupPage1
from gui.usersetup_page.us_pg2 import OccupationSelection as SetupPage2
from gui.usersetup_page.us_pg3 import AppearanceSelection as SetupPage3

class BaseSetupPage(QWidget):
    def __init__(self, message_widget: QWidget, content_widget: QWidget):
        super().__init__()

        self.message_widget = MessageFrame(message_widget)
        self.content_widget = ContentFrame(content_widget)

        main_layout = QHBoxLayout(self)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(self.message_widget)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(self.content_widget)

        main_layout.addWidget(left, 2)
        main_layout.addWidget(right, 3)

    def set_navigation_bar(self, nav_bar: QWidget):
        """Injected by manager each time page is shown."""
        self.content_widget.set_navigation(nav_bar)


class Page1(BaseSetupPage):
    def __init__(self):
        super().__init__(
            message_widget=FormMessage(),
            content_widget=SetupPage1(),
        )

class Page2(BaseSetupPage):
    def __init__(self):
        super().__init__(
            message_widget=OccupationMessage(),
            content_widget=SetupPage2(),
        )

class Page3(BaseSetupPage):
    def __init__(self):
        super().__init__(
            message_widget=AppearanceMessage(),
            content_widget=SetupPage3(),
        )
