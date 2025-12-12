# nav_bar_module.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, Signal, QPropertyAnimation, QObject
from pathlib import Path
import sys
import os

from core.signal_manager import marketplace_eb

# --- ICON PATHS ---
def icon_path(asset_name):
    # This path is retained from your original code
    base_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "marketplace_icons"
    full_path = base_dir / asset_name 
    
    # Fallback to a dummy path for runnable code
    placeholder_path = Path.cwd() / "dummy_icon.png"
    if not full_path.exists():
        if not placeholder_path.exists():
             try:
                 with open(placeholder_path, 'w') as f:
                     pass
             except Exception:
                 pass
        return str(placeholder_path)
        
    return str(full_path)


# Generic QPushButton with hover icon and selection logic
class IconButton(QPushButton):
    def __init__(self, name, default_icon_path, hover_icon_path, size=QSize(48, 48), parent=None):
        super().__init__(parent)
        self.button_name = name
        self.default_icon = QIcon(str(default_icon_path))
        self.hover_icon = QIcon(str(hover_icon_path))
        self._is_selected = False 
        
        self.setFixedSize(size)
        icon_dim = min(size.width(), size.height()) - 24  
        self.setIconSize(QSize(icon_dim, icon_dim))
        self.setFlat(True)
        self.setIcon(self.default_icon)

        self.setProperty("selected", "false")
        self._set_style()
        
    def _set_style(self):
        style_sheet = f"""
            IconButton {{
                background-color: transparent; 
                border: none;
                border-radius: {self.width() // 2}px;
                transition: background-color 0.2s; 
            }}
            
            IconButton:hover {{
                background-color: rgba(255, 255, 255, 0.2); 
            }}
            
            IconButton[selected="true"] {{
                background-color: white; /* Ensures blue background shows */
            }}
        """
        self.setStyleSheet(style_sheet)
        
    def set_selected(self, state):
        self._is_selected = state
        self.setProperty("selected", str(state).lower()) 
        self.style().polish(self)
        self.setIcon(self.hover_icon if state else self.default_icon)
        
    def enterEvent(self, event):
        if self._is_selected: return 
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._is_selected: return 
        self.setIcon(self.default_icon)
        super().leaveEvent(event)


# --- WRAPPER WIDGET TO DISPLAY NAME AND HANDLE EXPANSION ---

class NavItem(QWidget):
    clicked_item = Signal(QWidget) 
    
    def __init__(self, button_class, parent=None):
        super().__init__(parent)
        
        self.icon_button = button_class(parent=self)
        self.label = QLabel(self.icon_button.button_name, self)
        
        self.icon_width = self.icon_button.width() + 10
        self.text_width = self.label.fontMetrics().horizontalAdvance(self.icon_button.button_name) + 20
        self.expanded_width = self.icon_width + self.text_width

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.main_layout.setSpacing(5)
        
        self.main_layout.addWidget(self.icon_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch(1)

        self.setFixedWidth(self.icon_width)
        self.label.setVisible(False) 
        
        # Text color is white to contrast with the light blue background
        self.label.setStyleSheet("color: white; font-weight: bold;") 
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.setStyleSheet(self._base_style())
        
        self.icon_button.clicked.connect(self._emit_click)
        
    def _base_style(self):
        return """
            NavItem {
                background-color: transparent;
                border-radius: 20px;
            }
        """

    def _selected_style(self):
        # FIX: The NavItem should be transparent to show the blue frame beneath
        return """
            NavItem {
                background-color: transparent; 
                border-radius: 20px;
            }
        """
        
    def _emit_click(self):
        self.clicked_item.emit(self) 
        
    def set_selected(self, state):
        self.icon_button.set_selected(state)
        self.label.setVisible(state) 
        
        if state:
            self.setStyleSheet(self._selected_style())
            self._animate_width(self.expanded_width)
        else:
            self.setStyleSheet(self._base_style())
            self._animate_width(self.icon_width)

    def _animate_width(self, target_width):
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(150)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.start()
        self.setFixedWidth(target_width)


# --- ICON SUBCLASSES ---
class HomeIcon(IconButton):
    def __init__(self, parent=None):
        # Changed class names to avoid collision with Page names
        super().__init__("Home", icon_path("home_icon.svg"), icon_path("home_hover_icon.svg"), parent=parent)

class AppsIcon(IconButton):
    def __init__(self, parent=None):
        super().__init__("Apps", icon_path("apps_icon.svg"), icon_path("apps_hover_icon.svg"), parent=parent)

class ExploreIcon(IconButton):
    def __init__(self, parent=None):
        super().__init__("Explore", icon_path("explore_icon.svg"), icon_path("explore_hover_icon.svg"), parent=parent)

class InstalledIcon(IconButton):
    def __init__(self, parent=None):
        super().__init__("Installed", icon_path("installedapps_icon.svg"), icon_path("installedapps_hover_icon.svg"), parent=parent)


# --- NAV BAR MAIN CLASS ---
class NavBar(QWidget):
    
    def __init__(self):
        super().__init__()
        self.current_selection = None
        
        # Blue rounded area (QFrame)
        nav_frame = QFrame(self)
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #4fc3f7; /* Light Blue */
                border-radius: 20px;
            }
        """)
        
        # Horizontal layout inside the blue frame
        self.nav_layout = QHBoxLayout(nav_frame) 
        self.nav_layout.setContentsMargins(10, 10, 10, 10)
        self.nav_layout.setSpacing(5)
        
        # Initialize buttons wrapped in NavItem
        self.home_item = NavItem(HomeIcon, parent=nav_frame)
        self.apps_item = NavItem(AppsIcon, parent=nav_frame)
        self.explore_item = NavItem(ExploreIcon, parent=nav_frame)
        self.installed_item = NavItem(InstalledIcon, parent=nav_frame)
        
        self.items = [self.home_item, self.apps_item, self.explore_item, self.installed_item]

        for item in self.items:
            self.nav_layout.addWidget(item)
            # Connect NavItem's internal click signal to the NavBar's handler
            item.clicked_item.connect(self._handle_selection)

        self.nav_layout.addStretch(1)

        # Main layout for this NavBar widget
        main_v_layout = QVBoxLayout(self)
        main_v_layout.addWidget(nav_frame)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        
        # Set default selection
        self._handle_selection(self.home_item) 

    def _handle_selection(self, new_selection):
        """Manages the single selection state and emits a signal to the manager."""
        
        # Deselect the previous button
        if self.current_selection is not None and self.current_selection != new_selection:
            self.current_selection.set_selected(False)
            
        # Select the new button
        self.current_selection = new_selection
        self.current_selection.set_selected(True)
        
        # Emit signal with the page name (e.g., "Home", "Apps", "Explore", "Installed")
        marketplace_eb.nav_selection_page.emit(new_selection.icon_button.button_name)