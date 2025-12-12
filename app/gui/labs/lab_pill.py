from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPixmap, QFontMetrics # <--- QFontMetrics is added
import sys


try:
    from core.signal_manager import Lab_eb, Pill_eb
except ImportError:
    # Placeholder for running standalone
    class MockLab_eb:
        def __init__(self):
            pass
    class MockPill_eb:
        def __init__(self):
            pass
    
    Lab_eb = MockLab_eb()
    Pill_eb = MockPill_eb()

# ----------------------------------------
# 1) PillContentWidget: icon + name + cross button
# ----------------------------------------
class PillContentWidget(QWidget):
    cross_clicked = Signal()



    def __init__(self, icon_path: str = None, text: str = None, parent=None, lab_id: str = None):
        super().__init__(parent)

        self.lab_id = lab_id
        self.icon_path = icon_path if icon_path else None
        self.text_value = text if text else "Untitled Lab"

        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 0, 6, 0)
        self.layout.setSpacing(4)

        # Icon
        self.icon_label = QLabel()
        pix = QPixmap(self.icon_path) if self.icon_path else None
        if pix and not pix.isNull():
            self.icon_label.setPixmap(pix.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Placeholder/Fallback for missing icon
            placeholder = QPixmap(18, 18)
            placeholder.fill(QColor('#FFFFFF')) # White fallback is better
            self.icon_label.setPixmap(placeholder)
        self.layout.addWidget(self.icon_label)

        # Text Label
        self.text_label = QLabel(self.text_value)
        
        # --- FIX: Removed setTextElideMode (Not available on QLabel) ---
        # Set horizontal policy to Fixed so layout respects setFixedWidth
        self.text_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.text_label.setStyleSheet("""
            QLabel {
                font-size: 13px; 
                color: #000000;
            }
        """)
        self.layout.addWidget(self.text_label)

        # Spacer to push cross button to right
        self.layout.addStretch()

        # Cross Button
        self.cross_btn = QPushButton('×')
        self.cross_btn.setFixedSize(20, 20)
        self.cross_btn.setCursor(Qt.PointingHandCursor)
        self.cross_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: grey;
                font-weight: bold;
                font-size: 16px; /* Slightly larger for better touch target */
            }
            QPushButton:hover {
                background: rgba(255,0,0,0.2);
                color: red;
                border-radius: 8px;
            }
        """)
        self.layout.addWidget(self.cross_btn)

        # self.cross_btn.clicked.connect(lambda x: print('Lab closed'))
        self.cross_btn.clicked.connect(lambda: Lab_eb.close_lab.emit(self.lab_id))
    


    # Methods to show/hide text
    def show_text(self):
        # When showing text (pill is selected), set explicit width 
        fixed_width = 100 
        self.text_label.setFixedWidth(fixed_width) 
        
        # --- NEW: Manually truncate text using QFontMetrics ---
        metrics = QFontMetrics(self.text_label.font())
        truncated_text = metrics.elidedText(
            self.text_value, 
            Qt.ElideRight, 
            fixed_width
        )
        self.text_label.setText(truncated_text)
        self.text_label.show()

    def hide_text(self):
        self.text_label.hide()
        # Reset width when hidden
        self.text_label.setFixedWidth(0) 


# ----------------------------------------
# 2) LabPill: Outer pill + background + states (Normal Lab Style)
# ----------------------------------------
class LabPill(QWidget):
    # lab_type parameter kept for future compatibility, but style is fixed to 'normal'
    def __init__(self, icon_path: str = None, text: str = None, lab_id = None, parent=None):
        super().__init__(parent)
        
        self.lab_id = lab_id 
        # print("Lab ID2:", self.lab_id)

        self.height = 34
        self.unselected_width = 60
        self.selected_width = 160
        self.radius = self.height // 2

        self.is_selected = False
        self.is_hovered = False

        self.setFixedHeight(self.height)
        self.setMinimumWidth(self.unselected_width)
        self.setMaximumWidth(self.selected_width)
        self.setMouseTracking(True)

        # Background colors adapted for normal labs only
        self.color_selected = QColor('#D8EAFF') # Selected state is light blue
        
        # Unselected colors blend with the window background (#F7F7F7)
        self.color_unselected = QColor('#F7F7F7') 
        self.color_hover = QColor('#EEEEEE') 

        # Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 0, 4, 0)
        self.layout.setSpacing(0)

        # Content widget
        self.content = PillContentWidget(icon_path, text, lab_id=self.lab_id)
        self.layout.addWidget(self.content)

        # Start in unselected state
        self.update_state()

    # Hover events
    def enterEvent(self, event):
        if not self.is_selected:
            self.is_hovered = True
            self.update_state()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.is_hovered = False
            self.update_state()
        super().leaveEvent(event)

    # Click to select
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Emit select signal (handled externally by LabHostBar)
            Lab_eb.active_lab.emit(self.lab_id)
        super().mousePressEvent(event)
        
    # Public method to manually set selection state (called by LabHostBar)
    def set_selected(self, state: bool):
        self.is_selected = state
        self.update_state()


    # Update pill appearance based on state
    def update_state(self):
        # Width
        width = self.selected_width if self.is_selected else self.unselected_width
        self.setFixedWidth(width)

        # Background color
        if self.is_selected:
            color = self.color_selected
        elif self.is_hovered:
            color = self.color_hover
        else:
            color = self.color_unselected

        self.bg_color = color

        # Show/hide text label
        if self.is_selected:
            self.content.show_text()
        else:
            self.content.hide_text()

        self.update()

    # Paint pill
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)
        painter.end()


# ----------------------------------------
# 3) IncogLabPill: New Class with Grey Styling and Dual Icons
# ----------------------------------------
class IncogLabPill(QWidget):
    """
    A specialized LabPill with a fixed grey color scheme 
    and dual icons for Incognito mode.
    """
    def __init__(self, icon_path: str = None, text: str = None, parent=None, lab_id: str = None):
        super().__init__(parent)

        self.lab_id = lab_id
        
        # --- Dimensions and State ---
        self.height = 34
        self.unselected_width = 70 # Slightly wider for dual icons
        self.selected_width = 170
        self.radius = self.height // 2

        self.is_selected = False
        self.is_hovered = False

        self.setFixedHeight(self.height)
        self.setMinimumWidth(self.unselected_width)
        self.setMaximumWidth(self.selected_width)
        self.setMouseTracking(True)

        # --- Grey Color Scheme (Fixed) ---
        # 1. It have only grey color for all move (minimum, hover, maximum)
        self.color_unselected = QColor('#EAEAEA') 
        self.color_hover = QColor('#DADADA') 
        self.color_selected = QColor('#CFCFCF') # Slightly darker grey when selected

        # --- Layout and Content ---
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 0, 4, 0)
        self.layout.setSpacing(0)
        
        # Internal Content Widget (similar to PillContentWidget logic)
        
        # Dual Icon Requirement: 1. Default Icon
        # Using an emoji/character as a visual placeholder for the Incognito/Mask icon
        self.default_icon_label = QLabel("🕶") 
        self.default_icon_label.setStyleSheet('font-size: 14px; color: #444444;')
        self.layout.addWidget(self.default_icon_label)
        
        # Dual Icon Requirement: 2. Input Icon (Dynamic Session Icon)
        self.dynamic_content = PillContentWidget(icon_path, text, parent=self, lab_id=self.lab_id)
        self.dynamic_content.text_label.setStyleSheet('font-size: 13px; color: #000000; margin-left: -5px;') # Adjust alignment
        self.layout.addWidget(self.dynamic_content)
        
        # Re-map the cross-clicked signal from the inner widget
        self.cross_clicked = self.dynamic_content.cross_clicked
        
        # Start in unselected state
        self.update_state()

    # --- System is same as normal pill ---
    # Hover events
    def enterEvent(self, event):
        if not self.is_selected:
            self.is_hovered = True
            self.update_state()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.is_hovered = False
            self.update_state()
        super().leaveEvent(event)

    # Click to select
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'pill_clicked_callback'):
                self.pill_clicked_callback(event)
        super().mousePressEvent(event)
        
    def set_selected(self, state: bool):
        self.is_selected = state
        self.update_state()

    # Update pill appearance based on state
    def update_state(self):
        # Width
        width = self.selected_width if self.is_selected else self.unselected_width
        self.setFixedWidth(width)
        
        # Background color
        if self.is_selected:
            color = self.color_selected
        elif self.is_hovered:
            color = self.color_hover
        else:
            color = self.color_unselected

        self.bg_color = color

        # Show/hide text label
        if self.is_selected:
            self.dynamic_content.show_text()
        else:
            self.dynamic_content.hide_text()

        self.update()

    # Paint pill
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)
        painter.end()

