from PySide6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QPixmap


# -----------------------------
# Hoverable App Item with Animation
# -----------------------------
class HoverAppItem(QWidget):
    def __init__(self):
        super().__init__()
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(120)

    def enterEvent(self, event):
        r = self.geometry()
        self.anim.stop()
        self.anim.setStartValue(r)
        self.anim.setEndValue(QRect(r.x()-3, r.y()-3, r.width()+6, r.height()+6))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        r = self.geometry()
        self.anim.stop()
        self.anim.setStartValue(r)
        self.anim.setEndValue(QRect(r.x()+3, r.y()+3, r.width()-6, r.height()-6))
        self.anim.start()
        super().leaveEvent(event)


# -----------------------------
# Quick Access App Bar
# -----------------------------
class QuickAccessAppBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("partOne")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area (NO SCROLLBARS)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(130)  # Icon + text
        scroll.setStyleSheet("background: transparent; border: none;")

        # Container inside scroll
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(15)

        # --- Example Apps ---
        for i in range(20):
            item = self._create_app_item(f"App {i+1}")
            content_layout.addWidget(item)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # ---------- Style ----------
        self.setStyleSheet("""
            QWidget#partOne {
                background-color: #f6f6f6;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
            QLabel#appIcon {
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #ccc;
            }
            QLabel#appName {
                font-size: 13px;
                color: black;
            }
        """)

    # ---------------------------------------------------------
    # Create one APP item (icon + name)
    # ---------------------------------------------------------
    def _create_app_item(self, name: str) -> QWidget:
        item = HoverAppItem()
        item.setFixedSize(80, 100)

        layout = QVBoxLayout(item)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        # Icon (placeholder)
        icon_label = QLabel()
        icon_label.setObjectName("appIcon")
        icon_label.setFixedSize(60, 60)
        pix = QPixmap(60, 60)
        pix.fill("#e0e0e0")
        icon_label.setPixmap(pix)

        # Name
        name_label = QLabel(name)
        name_label.setObjectName("appName")
        name_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)

        return item
