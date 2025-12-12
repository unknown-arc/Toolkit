import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette

# import ctypes
# from ctypes import wintypes
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout,
#     QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame
# )
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QPalette, QPixmap, QPainter



# # --- Get current script directory ---
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # --- File to check (relative to launcher) ---
# file_to_check = os.path.join(current_dir, "user_data", "file.txt")  # Replace "file.txt" with your target

# # --- Path to main.py (inside subfolder) ---
# user_setup = os.path.join(current_dir, "user_setup", "main.py")  # Adjust subfolder name

# app_gui = os.path.join(current_dir, "gui","gui.py")  # Main app path

# # --- Check if file exists ---
# if not os.path.exists(file_to_check):
#     print(f"File not found: {file_to_check}")
#     print("Launching the main app...")
#     subprocess.run([sys.executable, user_setup])
# else:
#     subprocess.run([sys.executable, app_gui])


from app.app import App





from pathlib import Path

from app.user_profile_handler.profile_manager import ProfileManager


def user_setup():
    setup_script = Path(__file__).parent / "user_setup" / "main.py"   
    # Runs setup as a SEPARATE process
    subprocess.Popen(["python", str(setup_script)])

def get_profile():
    handler_dir = Path(__file__).parent / "app" / "user_profile_handler"
    manager = ProfileManager(handler_dir)
    result = manager.get_profile()

    if result == "No profile":
        user_setup()
        exit()
    elif result == "All profiles are corrupt":
        user_setup()
        exit()
    else:
        return result



app.profile_path = profile        


def main():
    profile_path =get_profile()     
    setup_script = Path(__file__).parent / "app" / "app.py" 
    subprocess.Popen(["python", str(setup_script)])   

if __name__ == "__main__":
    get_profile()
    main()


  



from app.app import App





from pathlib import Path

from app.user_profile_handler.profile_manager import ProfileManager


def user_setup():
    setup_script = Path(__file__).parent / "user_setup" / "main.py"   
    # Runs setup as a SEPARATE process
    subprocess.Popen(["python", str(setup_script)])

def get_profile():
    handler_dir = Path(__file__).parent / "app" / "user_profile_handler"
    manager = ProfileManager(handler_dir)
    result = manager.get_profile()

    if result == "No profile":
        user_setup()
        exit()
    elif result == "All profiles are corrupt":
        user_setup()
        exit()
    else:
        return result
      


def main():
    profile_path = get_profile()

    setup_script = Path(__file__).parent / "app" / "app.py"
    print("profile_path:", profile_path)

    subprocess.Popen([
        sys.executable,
        str(setup_script),
        str(profile_path)
    ])
 

if __name__ == "__main__":
    get_profile()
    main()


  

# def main():
#     app = QApplication(sys.argv)

#     profile = get_profile()
#     app.profile_path = profile

#     from app.app import App
#     win = App()
#     win.show()

#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()