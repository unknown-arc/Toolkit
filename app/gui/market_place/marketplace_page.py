from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QEvent

from .header_frame import HeaderFrame
from .content_frame import ContentFrame

from core.marketplace_manager.marketplace_manager import MarketplaceManager

class MarketPlacePage(QWidget):
    def __init__(self):
        super().__init__()

        self.header = HeaderFrame()
        self.manager = MarketplaceManager()
        self.content = self.manager.content_frame

        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Install global wheel listener
        self.installEventFilter(self)

        # scroll amount tracker
        self.scroll_progress = 0
        self.max_collapse = 3000  # pixels of "virtual" scroll

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            delta = event.angleDelta().y()

            # mouse scroll up (expand header)
            if delta > 0:
                self.scroll_progress = max(0, self.scroll_progress - abs(delta))
            # mouse scroll down (collapse header)
            else:
                self.scroll_progress = min(self.max_collapse, self.scroll_progress + abs(delta))

            # compute new height
            factor = self.scroll_progress / self.max_collapse
            new_height = self.header.max_height - (self.header.max_height - self.header.min_height) * factor
            self.header.setHeight(int(new_height))

            # Only scroll content when header is fully collapsed
            if self.scroll_progress >= self.max_collapse:
                return False  # allow normal content scrolling
            else:
                return True  # block content scroll

        return super().eventFilter(obj, event)
