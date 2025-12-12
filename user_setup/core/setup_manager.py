from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from core.event_signal import page_nav_sgl

from gui.frames.content_frame import ContentFrame
from gui.frames.message_frame import MessageFrame
from gui.widget.navigation_bar import NavigationBar

# user pages
from gui.usersetup_page.us_pg1 import UserInfoForm as Page1
from gui.usersetup_page.us_pg2 import OccupationSelection as Page2
from gui.usersetup_page.us_pg3 import AppearanceSelection as Page3

# side messages
from gui.messages.setupmessage import FormMessage as Msg1
from gui.messages.setupmessage import AppearanceMessage as Msg2
from gui.messages.setupmessage import AppearanceMessage as Msg3


class UserSetupManager(QWidget):
    def __init__(self, nav_height: int = 60):
        super().__init__()

        self.nav_height = nav_height
        self.current_index = 0
        self.pages_count = 3

        # visited is optional (for analytics)
        self.visited = [False] * self.pages_count

        # ⚠️ MAIN IMPORTANT FLAG — determines Next/Continue
        self.completed = [False] * self.pages_count   # modified ONLY in on_continue()

        # root layout
        self.root_layout = QHBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # left = message, right = content
        self.left_container = QWidget()
        self.right_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.right_layout = QVBoxLayout(self.right_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        self.root_layout.addWidget(self.left_container)
        self.root_layout.addWidget(self.right_container)

        # instances of pages/messages/navbars
        self.pages = [Page1(), Page2(), Page3()]
        self.messages = [Msg1(), Msg2(), Msg3()]

        self.content_frames = []
        self.message_frames = []
        self.navbars = []

        for i in range(self.pages_count):
            nav = NavigationBar(idx=i)
            nav.setFixedHeight(nav_height)

            content = ContentFrame(self.pages[i], nav)
            message = MessageFrame(self.messages[i])

            self.navbars.append(nav)
            self.content_frames.append(content)
            self.message_frames.append(message)

        # connect signals
        page_nav_sgl.back_sgl.connect(self.go_back)
        page_nav_sgl.next_sgl.connect(self.go_next)
        page_nav_sgl.continue_sgl.connect(self.on_continue)

        # load first page
        self.load_page(0)

    def load_page(self, idx: int):
        # clear layouts
        self.clear_layout(self.left_layout)
        self.clear_layout(self.right_layout)

        self.current_index = idx
        page_completed = self.completed[idx]
        is_last = (idx == self.pages_count - 1)
        self.visited[idx] = True  # for analytics only

        msg = self.message_frames[idx]
        content = self.content_frames[idx]
        nav = self.navbars[idx]

        # show/hide back
        nav.back_btn.setVisible(idx > 0)

        # continue vs next (MAIN LOGIC)
        if page_completed:
            # This page was completed earlier → show NEXT
            nav.continue_btn.setVisible(False)
            nav.next_btn.setVisible(not is_last)
        else:
            # Not completed yet → show CONTINUE
            nav.next_btn.setVisible(False)
            nav.continue_btn.setVisible(True)

        # add widgets (2:3 split)
        self.left_layout.addWidget(msg)
        self.right_layout.addWidget(content)

        self.root_layout.setStretchFactor(self.left_container, 2)
        self.root_layout.setStretchFactor(self.right_container, 3)

    def on_continue(self):
        """Continue button pressed on THIS page."""
        idx = self.current_index
        page = self.content_frames[idx]

        # if page has validation
        if hasattr(page, "on_continue"):
            ok = page.on_continue()
            if ok is False:
                return

        # if page provides data
        if hasattr(page, "get_data"):
            data = page.get_data()
            # save it somewhere if needed

        # mark THIS page as completed
        self.completed[idx] = True

        # load next page
        self.go_next()

    def go_next(self):
        if self.current_index < self.pages_count - 1:
            self.load_page(self.current_index + 1)

    def go_back(self):
        if self.current_index > 0:
            self.load_page(self.current_index - 1)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
