# core/lab_controller.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

if __name__ == "__main__":
    from pathlib import Path
    import sys
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    print("Root dir:", ROOT_DIR)     

    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    print("Root dir:", ROOT_DIR)     

from core.lab_and_session_manager.lab_id import generate_lab_id
from core.subapp_manager.get_app import GetAppInfo
from core.signal_manager import Lab_eb, LeftPanel_eb, Session_eb, Pill_eb

class LabManager:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.labs: Dict[str, Dict] = {}
        self.active_lab: str | None = None
        self.quicklab_counter = 0

        LeftPanel_eb.new_lab.connect(self.new_lab)
        LeftPanel_eb.incognito_lab.connect(self.incognito_lab)
        LeftPanel_eb.close_all_labs.connect(self.close_all_labs)

        Lab_eb.add_lab.connect(self.add_lab)
        # Lab_eb.close_lab.connect(lambda x : print("Closing lab:", x))
        Lab_eb.close_lab.connect(self.close_lab)
        Lab_eb.active_lab.connect(self.set_active)
        # Lab_eb.active_lab.connect(lambda x : print("Closing lab:", x))
        Lab_eb.rename_lab.connect(self.lab_rename_request)

  

    def new_lab(self, lab_title: str | None = None, app_id: str | None = None):
        lab_id = generate_lab_id()
        name = lab_title if lab_title else "Untitled Lab"
        app_id = app_id if app_id else "quicklab"        
        app_icon = "Z:\\Project\\Toolkit\\app\\assets\\leftpanel_icons\\newlab.svg"
        self.labs[lab_id] = {
            "title": name,
            "app_id": app_id,
            "icon": app_icon
            }
        Pill_eb.new_pill.emit({"id": lab_id, "title": name, "icon": app_icon})
        Session_eb.add_session.emit({"id": lab_id, "title": name, "app_id": app_id, "content": "quicklab"})

        return lab_id


    def add_lab(self, app_id: str):
        lab_id = generate_lab_id()
        if app_id == "quicklab" or app_id == "":
            new_lab()
        else: 
            app_info = GetAppInfo(app_id, self.profile_path).get_app_info()
            self.labs[lab_id] = {
                "app_id": app_info.get("id"),
                "name": app_info.get("name"),
                "main": app_info.get("main"),
                "info": app_info.get("info"),
                "icon": app_info.get("icon"),
            }

            Pill_eb.add_pill.emit({"id": lab_id, "title": app_info.get("name"), "icon": app_info.get("icon")})
            Session_eb.add_session.emit({"id": lab_id, "title": app_info.get("name"), "content": app_info.get("main"), "app_id": app_id})

    

    def incognito_lab(self, content: str):
        lab_id = generate_lab_id()
        if content == "quicklab" or content == "":
            title = f"Incognito Lab"

        self.labs[lab_id] = {
            "title": title, 
            "content": content, 
            "code_used": False
            }
        Pill_eb.incognito_pill.emit({"id": lab_id, "title": title})
        Session_eb.add_session.emit({"id": lab_id, "title": title, "type": content, "content": content})

    def close_lab(self, lab_id: str):
        if lab_id in self.labs:
            self.labs.pop(lab_id)
            Pill_eb.remove_pill.emit(lab_id)
            Session_eb.close_session.emit(lab_id)

            if self.active_lab == lab_id:
                if self.labs:
                    self.set_active(next(iter(self.labs)))
                else:
                    self.active_lab = None

    def set_active(self, lab_id: str):
        if lab_id in self.labs:
            self.active_lab = lab_id
            Pill_eb.active_pill.emit(lab_id)
            Session_eb.active_session.emit(lab_id)

    def update_lab_content(self, lab_id: str, content: str):
        if lab_id in self.labs:
            self.labs[lab_id]["content"] = content

    def lab_rename_request(self, lab_id: str, rename_title: str):
        if lab_id not in self.labs:
            return
        lab_data = self.labs[lab_id]
        if lab_data.get("title") == "Untitled Lab" and not lab_data.get("code_used"):
            self.quicklab_counter += 1
            final_title = f"Lab {self.quicklab_counter}"
            lab_data["title"] = final_title
            lab_data["code_used"] = True
        else:
            lab_data["title"] = rename_title

        Pill_eb.rename_pill.emit({"id": lab_id, "new_title": lab_data["title"]})
        Session_eb.rename_session.emit({"id": lab_id, "new_title": lab_data["title"]})

    def close_all_labs(self):
        self.labs.clear()
        self.active_lab = None
        Pill_eb.remove_all_pills.emit()
        Session_eb.close_all_sessions.emit()