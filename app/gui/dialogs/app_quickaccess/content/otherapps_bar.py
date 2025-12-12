# part_two_widget.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea,
    QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class OtherApps(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("partTwo")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ───────────────────────────────────────────────
        # Scroll Area (Vertical)
        # ───────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setSpacing(12)

        # ───────────────────────────────────────────────
        # Sample 40 app boxes
        # ───────────────────────────────────────────────
        row = 0
        col = 0
        for i in range(40):
            app_box = self.create_app_item(f"App {i+1}")
            grid.addWidget(app_box, row, col)

            col += 1
            if col >= 5:   # 4 items per row
                col = 0
                row += 1

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # ───────────────────────────────────────────────
        # Modern Scrollbar Style
        # ───────────────────────────────────────────────
        self.setStyleSheet("""
            /* -------------------------
                Modern Scrollbar
            ------------------------- */
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #c9c9c9;
                min-height: 30px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #b5b5b5;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }

            /* -------------------------
            App Box (Normal)
            ------------------------- */
            QWidget#appBox {
                background: white;
                border-radius: 12px;
                border: 1px solid #ddd;
                transition: all 120ms ease;
            }

            /* -------------------------
            App Box Hover Effect
            ------------------------- */
            QWidget#appBox:hover {
                background: #f1f1f1;
                border: 1px solid #bbb;
                transform: scale(1.05);
            }

            QLabel#appIcon {
                background: #e9e9e9;
                border-radius: 8px;
            }

            QLabel#appName {
                color: #333;
                font-size: 13px;
            }
        """)


    # ───────────────────────────────────────────────
    # App Item Widget
    # ───────────────────────────────────────────────
    def create_app_item(self, name):
        box = QWidget()
        box.setFixedSize(120, 120)
        box.setObjectName("appBox")

        v = QVBoxLayout(box)
        v.setAlignment(Qt.AlignCenter)
        v.setContentsMargins(8, 8, 8, 8)

        # placeholder icon
        icon = QLabel()
        icon.setFixedSize(60, 60)
        icon.setObjectName("appIcon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setText("📦")

        # app name
        lbl = QLabel(name)
        lbl.setObjectName("appName")
        lbl.setAlignment(Qt.AlignCenter)

        v.addWidget(icon)
        v.addWidget(lbl)

        return box
