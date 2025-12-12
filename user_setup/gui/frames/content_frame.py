from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt


class ContentFrame(QWidget):
    def __init__(self, content_widget: QWidget, nav_bar:QWidget = None, idx_bar: QWidget = None, parent=None):
        
        super().__init__(parent)

        # Styles
        self.setStyleSheet("""

            QWidget#root_bg {
                background-color: #ffffff; /* Light gray background for window */
            }
            QFrame#content_bg {
                background-color: #ffffff;
            }

            QFrame#card {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 16px;
                padding: 40px;
            }

            """)

            
        # self.setWindowTitle("App")
        # self.resize(900, 600)


        # --------------- Main Layout (Root) ---------------
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- CONTENT AREA ----------
        content = QFrame()
        content.setObjectName("content_bg")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignCenter)

        # Card Container
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(20)


        if idx_bar is not None:
            card_layout.addWidget(idx_bar, alignment=Qt.AlignTop)

        content_widget.setMaximumWidth(420)
        card_layout.addWidget(content_widget, alignment=Qt.AlignCenter)
        
        if nav_bar is not None:
            card_layout.addWidget(nav_bar, alignment=Qt.AlignBottom)

        content_layout.addWidget(card, alignment=Qt.AlignCenter)
        root_layout.addWidget(content, stretch=1)

    # inside ContentFrame class
    def replace_navbar(self, new_nav):
        # assume card_layout has the nav as last widget (as in your code)
        # remove old nav if present
        try:
            old = self.nav_bar
        except AttributeError:
            old = None

        if old is not None:
            # remove and delete old nav
            # search and remove from card layout
            card_layout = self.findChild(QVBoxLayout)  # safe alternative: store card_layout in self
            # simpler: just call layout().removeWidget on nav widget parents if you stored them
            old.setParent(None)

        # set and add new nav
        self.nav_bar = new_nav
        # add it the same place you previously did
        # (if you stored card_layout as self.card_layout, use that)
        self.card_layout.addWidget(self.nav_bar, alignment=Qt.AlignBottom)
