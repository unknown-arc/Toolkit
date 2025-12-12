from PySide6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QFrame, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter # Assuming these are needed for LabPill

from core.signal_manager import Pill_eb, Lab_eb
# Import both pill types (assuming these are defined/available)
from gui.labs.lab_pill import LabPill, IncogLabPill

class LabHostBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")

        self.pills = {} 
        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()
        self.scroll.setWidget(self.container)

        self.layout = QHBoxLayout(self.container)
        self.layout.setContentsMargins(10, 6, 10, 6)
        self.layout.setSpacing(6)
        self.layout.setAlignment(Qt.AlignLeft)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll)

        Pill_eb.new_pill.connect(self.on_new_lab)
        Pill_eb.add_pill.connect(self.on_add_lab)
        Pill_eb.remove_pill.connect(self.on_close_lab)
        Pill_eb.remove_all_pills.connect(self.on_close_all_labs)
        Pill_eb.incognito_pill.connect(self.add_incognito_lab)
        # Pill_eb.incognito_pill.connect(lambda x: print("hi",x))
        # Pill_eb.rename_pill.connect(self.on_rename_lab)
        Pill_eb.active_pill.connect(self.set_active_lab)

    def on_new_lab(self, info: dict):
        lab_id = info["id"] 
        title = info.get("title", "Untitled Lab")
        icon = info.get("icon")

        pill = LabPill(icon_path=icon, text=title, lab_id=lab_id)
        self._add_pill_to_hostbar(lab_id, pill)

        Lab_eb.active_lab.emit(lab_id) 

    def on_add_lab(self, info: dict):
        lab_id = info["id"]
        title = info.get("title")
        icon = info.get("icon")

        pill = LabPill(icon_path=info.get("icon"), text=info.get("title"), lab_id=lab_id)
        self._add_pill_to_hostbar(lab_id, pill)

        Lab_eb.active_lab.emit(lab_id)

    def add_incognito_lab(self, info: dict):
        lab_id = info["id"]
        title = info.get("title", "Incognito Lab")

        pill = IncogLabPill(icon_path=info.get("icon"), text=title, lab_id=lab_id)
        self._add_pill_to_hostbar(lab_id, pill)

        Lab_eb.active_lab.emit(lab_id) 

    
    def _add_pill_to_hostbar(self, lab_id: str, pill):
        self.pills[lab_id] = pill

        pill.pill_clicked_callback = lambda event, lid=lab_id: Lab_eb.active_lab.emit(lid)
        # Assuming cross button signal connection via pill.content or pill.cross_clicked
        if hasattr(pill, 'content'):
            pill.content.cross_clicked.connect(lambda lid=lab_id: Lab_eb.close_lab.emit(lid))
        elif hasattr(pill, 'cross_clicked'):
            pill.cross_clicked.connect(lambda lid=lab_id: Lab_eb.close_lab.emit(lid))

        self.layout.addWidget(pill) 

    def on_rename_lab(self, lab_id: str, new_title: str):
        """Updates the text on the pill when the controller confirms the rename."""
        pill = self.pills.get(lab_id)
        if pill and hasattr(pill.content, 'text_label'):
           
            pill.content.text_label.setText(new_title)
            pill.update_state()

    def set_active_lab(self, lab_id: str):
        for id_, pill in self.pills.items():
            pill.is_selected = (id_ == lab_id)
            pill.update_state()

    def on_close_lab(self, lab_id: str):
        pill = self.pills.pop(lab_id, None)
        if pill:
            pill.deleteLater()

    def on_close_all_labs(self):
        for lab_id, pill in list(self.pills.items()):
            self.layout.removeWidget(pill)   
            pill.deleteLater()               
            del self.pills[lab_id]           

            