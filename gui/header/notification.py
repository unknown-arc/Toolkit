import os
import sys
from PySide6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PySide6.QtCore import Qt, QSize, QRect

class NotificationButton(QPushButton):
    """
    A circular button widget designed to display a settings icon.
    It is flexible, adapting to the size provided by its parent layout.
    
    1. Imports image from the 'Toolkit/assest/' location based on the new structure.
    2. If it fails, covers the profile with gray color.
    3. Includes visual feedback when clicked.
    """
    
    # The name of the file this component expects in the 'assest' folder.
    # ASSET_FILENAME =
    ASSET_FILENAME = "setting_icon.png" 

    def __init__(self, preferred_size: int = 64):
        """
        Initializes the circular button.
        
        :param preferred_size: The preferred (but not fixed) width/height.
        """
        super().__init__()
        self._preferred_size = preferred_size 
        
        self._load_and_prepare_image()
        
        # Add a simple stylesheet to remove the default button border/background
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0;
            }
        """)
        self.setToolTip("Settings")

    def sizeHint(self) -> QSize:
        """
        Suggests a square size to the layout manager based on the preferred size.
        """
        return QSize(self._preferred_size, self._preferred_size)

    def _load_and_prepare_image(self):
        """
        Attempts to load the settings image using the project structure path.
        If loading fails or the file doesn't exist, it uses a gray fill color.
        """
        # --- PATH CALCULATION BASED ON NEW FOLDER STRUCTURE ---
        # setting.py is in Toolkit/gui/header/
        # Image is in Toolkit/assest/settings_icon.png
        
        # 1. Get the directory of the current file (header/)
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Go up three levels to the project root (Toolkit/)
        project_root = os.path.abspath(os.path.join(current_file_dir, '..', '..', '..'))
        
        # 3. Construct the full expected asset path
        asset_path = os.path.join(project_root, 'assest', self.ASSET_FILENAME)

        asset_path = r'Z:\Project\Toolkit\assests\notification.png'
        
        # --- END PATH CALCULATION ---

        image_loaded = False
        load_size = self._preferred_size * 2
        
        if os.path.exists(asset_path):
            try:
                temp_pixmap = QPixmap(asset_path)
                if not temp_pixmap.isNull():
                    self._original_pixmap = temp_pixmap.scaled(
                        load_size, load_size, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    image_loaded = True
            except Exception:
                pass 

        if not image_loaded:
            # Fallback to gray color as requested
            print(f"NotificationButton: Could not load image at {asset_path}. Using GRAY fallback.")
            self._original_pixmap = QPixmap(load_size, load_size)
            self._original_pixmap.fill(QColor("gray"))
            
    def paintEvent(self, event):
        """
        Handles the custom drawing. The image is scaled and clipped 
        based on the widget's CURRENT size, making it responsive.
        Adds visual feedback when the button is pressed down.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        current_size = min(rect.width(), rect.height())
        
        if current_size <= 0:
            painter.end()
            return
            
        # Ensure it's a circle by creating a circular clip path
        path = QPainterPath()
        path.addEllipse(rect)
        painter.setClipPath(path)
        
        # Scale the original pixmap to the current size of the widget
        scaled_pixmap = self._original_pixmap.scaled(
            current_size, current_size, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Draw the scaled pixmap (it will always fill the circle)
        painter.drawPixmap(rect.topLeft(), scaled_pixmap)
        
        # --- ADD VISUAL CLICK FEEDBACK ---
        if self.isDown():
            # Apply a semi-transparent dark overlay when the button is pressed
            overlay_color = QColor(0, 0, 0, 50) # Black with 50 alpha (about 20% opacity)
            painter.setBrush(overlay_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rect)
        # --- END VISUAL CLICK FEEDBACK ---
        
        painter.end()

if __name__ == '__main__':
    # Simple demo for the Settings Button
    app = QApplication(sys.argv)
    
    # --- DEMO SETUP ---
    # NOTE: In a complex file structure like this, the demo setup cannot reliably 
    # create the asset file in the 'Toolkit/assest' directory because the demo 
    # runs from the 'gui/header' directory and cannot create external folders.
    # Therefore, the demo will test the 'gray fallback' case by default.
    
    print(f"Due to complex directory structure, the demo will likely show the GRAY fallback.")
    print(f"To test image success, manually place a file named '{NotificationButton.ASSET_FILENAME}'")
    print(f"in your 'Toolkit/assest' directory and run main.py.")
    
    # Use QWidget as the container for this simple demo
    main_window = QWidget() 
    button = NotificationButton(preferred_size=40)
    
    # The button is already clickable, this connects the action
    button.clicked.connect(lambda: print("Settings Button Clicked!"))
    
    main_window.setFixedSize(60, 60)
    main_layout = QHBoxLayout(main_window)
    main_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
    
    main_window.setWindowTitle("Settings Button Demo (Asset Path Updated)")
    main_window.show()
    
    # Cleanup is removed as no dummy file is created locally.
    sys.exit(app.exec())
