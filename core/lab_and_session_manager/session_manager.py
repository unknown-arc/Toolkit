# session_manager.py

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QSizePolicy
from pathlib import Path
import sys

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

from gui.labs.lab_window import LabWindow
from core.signal_manager import Session_eb
from core.lab_and_session_manager.session_id import generate_session_id
from quick_lab.quick_lab import QuickLab  
from core.subapp_manager.load_app_for_session import load_app_widget 
from core.lab_and_session_manager.external_window import ExternalProcessWidget

class QuickLabSessionWidget(QWidget):
    def __init__(self, session_id, title):
        super().__init__()
        self.session_id = session_id
        self.title = title

        layout = QVBoxLayout(self)

        # 1. Create QuickLab instance
        self.quicklab = QuickLab()
        self.quicklab.lab_id = session_id
        self.quicklab.setWindowTitle(title)

        # 3. Add QuickLab UI inside this widget
        layout.addWidget(self.quicklab)


# Main LabWindow using session_id
class SessionManager(LabWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    
        self.session_container.setSizePolicy(
            QSizePolicy.Expanding, 
            QSizePolicy.Expanding
        )
        
        # 2. Tell the container's layout to activate and resize itself
        if self.session_layout:
             self.session_layout.activate()
        
        # 3. Request a layout update from the main window (self is SessionManager/LabWindow)
        self.updateGeometry() 

        # ... rest of the code ...
        if self.session_layout is None or not isinstance(self.session_layout, QVBoxLayout):
            print("CRITICAL DEBUG: self.session_layout is missing or invalid!")
        else:
            print("DEBUG: self.session_layout is valid.")    
        self.sessions = {}
        self.lab_to_session = {}

        # Signals
        Session_eb.add_session.connect(self.create_session)
        # Session_eb.add_session.connect(lambda x : print("Adding session:", x))
        Session_eb.close_session.connect(self.close_session)
        # Session_eb.close_session.connect(lambda x : print("Close session:", x))
        Session_eb.active_session.connect(self.active_session)
        Session_eb.rename_session.connect(self.rename_session)
        Session_eb.close_all_sessions.connect(self.close_all_sessions)

    # --------------------------------------------------------
    def get_or_create_session_id(self, lab_id: str) -> str:
        # If already exists → return existing session id
        if lab_id in self.lab_to_session:
            return self.lab_to_session[lab_id]

        # Otherwise create a new one
        session_id = generate_session_id()
        self.lab_to_session[lab_id] = session_id
        return session_id


    def create_session(self, info: dict):
        lab_id = info.get("id")
        app_id = info.get("app_id")
        title = info.get("title", f"Lab {lab_id}")
        content = info.get("content")

        # NEW: Get same session_id every time
        session_id = self.get_or_create_session_id(lab_id)
        print("Creating session:", session_id)

        # If session already exists → simply switch to it
        if session_id in self.sessions:
            self.switch_session(session_id)
            return

        # Otherwise create a new session widget
        if app_id == "quicklab":
            widget = QuickLabSessionWidget(session_id, title)

        else:
            # Attempt EMBED FIRST
            try:
                app_path = Path(content)
                app_widget = load_app_widget(app_path)

                # embed mode
                widget = QWidget()
                layout = QVBoxLayout(widget)
                layout.addWidget(app_widget)
                print(f"[OK] Loaded {app_id} INSIDE session window")

                self.sessions[session_id] = widget
                self.session_layout.addWidget(widget)
                return

            except Exception as e:
                print(f"[FAIL] Cannot embed {app_id}: {e}")
                print("[INFO] Launching external process window")

                # Create external process window
                external_window = ExternalProcessWidget(
                    app_path=Path(content),
                    app_name = title,
                    lab_id=lab_id,
                    session_id=session_id
                )
                # Add panel into lab window (this is just info panel, not the real app)
                self.sessions[session_id] = external_window
                self.session_layout.addWidget(external_window)

                print("[OK] External app launched, info shown inside session")
                return

    

        widget.session_id = session_id
        self.sessions[session_id] = widget

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.session_layout.addWidget(widget)


    # --------------------------------------------------------
    def active_session(self, lab_id: str):
        session_id = self.get_or_create_session_id(lab_id)
        # print("Switching to session:", session_id)
        for sid, widget in self.sessions.items(): 
            widget.setVisible(sid == session_id)

    # --------------------------------------------------------
    def close_session(self, lab_id: str):
        session_id = self.get_or_create_session_id(lab_id)
        widget = self.sessions.pop(session_id, None)
        if widget:
            widget.setParent(None)
            widget.deleteLater()
            Session_eb.session_closed.emit(session_id)

    # --------------------------------------------------------
    def close_all_sessions(self):
        for widget in self.sessions.values():
            widget.setParent(None)
            widget.deleteLater()
        self.sessions.clear()
        self.lab_to_session.clear()
        Session_eb.all_sessions_closed.emit()

    # --------------------------------------------------------
    def rename_session(self, info):
        lab_id = info.get("id")
        new_title = info.get("new_title")

        session_id = self.lab_to_session.get(lab_id)
        if not session_id:
            return

        widget = self.sessions.get(session_id)
        if widget:
            widget.title = new_title

    def _close_external_if_matches(self, session_id, widget):
        if widget and getattr(widget, "session_id", None) == session_id:
            widget._terminate_process()

