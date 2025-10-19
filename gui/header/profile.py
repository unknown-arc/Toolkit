import os
import sys
from PySide6.QtWidgets import (
    QApplication, 
    QPushButton, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout, # Added for better header simulation
    QLabel
)
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PySide6.QtCore import Qt, QSize, QRect

class UserProfile(QPushButton):
    """
    A circular button widget designed to display a user profile image.
    This version is designed to be flexible and adapt to the size provided 
    by its parent layout rather than using a fixed size.
    
    Compatible with PySide6.
    """
    
    # Define a dummy image path for demonstration purposes
    DUMMY_IMAGE_PATH = "./dummy_profile.png"

    def __init__(self, preferred_size: int = 64):
        """
        Initializes the circular button.
        
        :param preferred_size: The preferred (but not fixed) width/height. 
                              Used for the initial size hint and the internal pixmap scale.
        """
        super().__init__()
        # Store preferred size for sizeHint() and internal pixmap scaling
        self._preferred_size = preferred_size 
        
        # Load the image once into a stable _original_pixmap
        self._load_and_prepare_image()
        
        # Add a simple stylesheet to remove the default button border/background
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0;
            }
        """)

    def sizeHint(self) -> QSize:
        """
        Suggests a square size to the layout manager based on the preferred size.
        """
        return QSize(self._preferred_size, self._preferred_size)

    def _load_and_prepare_image(self):
        """
        Attempts to load the profile image from the dummy path.
        If loading fails or the file doesn't exist, it uses a black fill color.
        
        The resulting pixmap is stored in self._original_pixmap.
        """
        image_loaded = False
        
        # 3. Imports user profile for that circle from a dummy location
        # Use the preferred size for the internal image storage quality
        load_size = self._preferred_size * 2 # Load at a higher resolution for better scaling
        
        if os.path.exists(self.DUMMY_IMAGE_PATH):
            try:
                temp_pixmap = QPixmap(self.DUMMY_IMAGE_PATH)
                if not temp_pixmap.isNull():
                    # Scale the pixmap to cover the entire button size area
                    self._original_pixmap = temp_pixmap.scaled(
                        load_size, load_size, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    image_loaded = True
            except Exception:
                pass # Silently handle exceptions

        if not image_loaded:
            # 4. If import fails, fill user profile with black colour
            self._original_pixmap = QPixmap(load_size, load_size)
            self._original_pixmap.fill(QColor("black"))
            
    def paintEvent(self, event):
        """
        Handles the custom drawing. The image is scaled and clipped 
        based on the widget's CURRENT size, making it responsive.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Use the CURRENT width/height of the widget (rect())
        rect = self.rect()
        current_size = min(rect.width(), rect.height()) # Use the smaller dimension to maintain square aspect
        
        if current_size <= 0:
            painter.end()
            return
            
        # 1. Ensure it's a circle by creating a circular clip path
        path = QPainterPath()
        # Add an ellipse centered within the current rectangle
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
        
        painter.end()


# --- Demonstration Code ---

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- Setup for Demonstration ---
    
    # This path is used to test the success case (it will be created and contain a gray circle)
    SUCCESS_PATH = "./test_success_profile.png"
    # This path is guaranteed to fail, testing the black fallback
    FAILURE_PATH = "./non_existent_profile.png"
    
    # 1. Create a dummy image for the SUCCESS test (a simple gray square)
    try:
        success_pixmap = QPixmap(128, 128) # Create large source image
        success_pixmap.fill(QColor("gray"))
        success_pixmap.save(SUCCESS_PATH, "PNG")
        print(f"Dummy image created at: {SUCCESS_PATH}. The first button should show GRAY.")
    except Exception as e:
        print(f"Could not create dummy image: {e}. Both buttons might show BLACK.")
        
    main_window = QMainWindow()
    
    # --- Simulate a Header Widget (80px height) ---
    header_widget = QWidget()
    header_widget.setFixedHeight(80) # Fixed height, simulating a header
    header_widget.setStyleSheet("background-color: #f0f0f0;")
    
    header_layout = QHBoxLayout(header_widget)
    header_layout.setContentsMargins(10, 5, 10, 5) # Margin around the content
    
    # Left Content
    header_layout.addWidget(QLabel("App Title"), alignment=Qt.AlignmentFlag.AlignVCenter)
    
    # Spacer to push the button to the right
    header_layout.addStretch(1) 
    
    # --- Flexible Button in 80px space ---
    # Preferred size is 64, but the layout space will constrain it to roughly 70x70 
    # (80px height minus 5px top/bottom margin)
    
    # Temporarily set the class path to the success path
    UserProfile.DUMMY_IMAGE_PATH = SUCCESS_PATH
    # The button will automatically resize to fit the layout's available space (approx. 70x70)
    button_flexible = UserProfile(preferred_size=64) 
    button_flexible.clicked.connect(lambda: print("Flexible Button Clicked! (Should be about 70px)"))
    header_layout.addWidget(button_flexible, alignment=Qt.AlignmentFlag.AlignVCenter)

    # --- Button in a fixed, smaller space (Fallback Test) ---
    footer_widget = QWidget()
    footer_layout = QHBoxLayout(footer_widget)
    footer_layout.addStretch(1)
    
    UserProfile.DUMMY_IMAGE_PATH = FAILURE_PATH
    # This button is explicitly constrained to a smaller box by layout and will show black
    button_constrained = UserProfile(preferred_size=40)
    button_constrained.clicked.connect(lambda: print("Constrained Button Clicked! (Should be 40px, Black)"))
    button_constrained.setFixedSize(40, 40) # Demonstrate fixed size still works if used
    footer_layout.addWidget(button_constrained, alignment=Qt.AlignmentFlag.AlignRight)
    
    # --- Main Layout ---
    central_widget = QWidget()
    main_layout = QVBoxLayout(central_widget)
    main_layout.addWidget(header_widget)
    main_layout.addStretch(1)
    main_layout.addWidget(footer_widget)
    
    main_window.setCentralWidget(central_widget)
    main_window.setWindowTitle("Flexible Circular Profile Button Example")
    main_window.resize(600, 400)
    main_window.show()
    
    # --- Cleanup Function ---
    def cleanup():
        """Cleans up the temporary dummy file."""
        if os.path.exists(SUCCESS_PATH):
            os.remove(SUCCESS_PATH)
        # Restore the class path constant (good practice)
        UserProfile.DUMMY_IMAGE_PATH = "./dummy_profile.png"

    app.aboutToQuit.connect(cleanup)
    
    sys.exit(app.exec())
