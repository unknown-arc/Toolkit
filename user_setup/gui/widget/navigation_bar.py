# gui/widget/navigation_bar.py

from PySide6.QtWidgets import QWidget, QHBoxLayout
from gui.widget.common_buttons import BackButton, NextButton, ContinueButton
from core.event_signal import page_nav_sgl

class NavigationBar(QWidget):
    def __init__(self, idx: int = 0):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.back_btn = BackButton()
        self.continue_btn = ContinueButton()
        self.next_btn = NextButton()

        # Back button only if not first page
        layout.addWidget(self.back_btn) if idx > 0 else None
        layout.addStretch(1)

        # ADD BOTH BUTTONS ALWAYS ONCE
        layout.addWidget(self.continue_btn)
        layout.addWidget(self.next_btn)

        # both visible state handled externally
        self.continue_btn.hide()
        self.next_btn.hide()

        # connect signals
        self.back_btn.clicked.connect(page_nav_sgl.back_sgl.emit)
        self.next_btn.clicked.connect(page_nav_sgl.next_sgl.emit)
        self.continue_btn.clicked.connect(page_nav_sgl.continue_sgl.emit)
