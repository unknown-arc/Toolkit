from PySide6.QtWidgets import QDialog

from gui.get_help.gethelp_dialog import CustomDialog
from gui.dialogs.user_profile.userprofile_diagol import UserProfileDialog
from gui.dialogs.app_quickaccess.quickaccess_dialog import QuickAccessDialog 
from core.signal_manager import Header_eb, Quickaccess_eb

class DialogManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.dialogs = {}
        self.add_dailog()
        self.connect_signals()

    def add_dailog(self):
        self.register_dialog("get_help", CustomDialog)
        self.register_dialog("user_profile", UserProfileDialog)
        self.register_dialog("app_quickaccess", QuickAccessDialog)

    def register_dialog(self, name, dialog_class):
        """Register dialog class for lazy instantiation."""
        self.dialogs[name] = dialog_class

    def show_dialog(self, name, *args, **kwargs):
        """Instantiate and show a dialog with its name."""
        if name not in self.dialogs:
            raise ValueError(f"Dialog '{name}' is not registered.")
        
        dialog_class = self.dialogs[name]
        dialog = dialog_class(self.parent, *args, **kwargs)
        dialog.exec()

    def connect_signals(self):
        Header_eb.open_gethelp_dialog.connect(lambda: self.show_dialog("get_help"))
        Header_eb.open_userprofile_dialog.connect(lambda: self.show_dialog("user_profile"))  
        Quickaccess_eb.open_quickaccess_dialog.connect(lambda: self.show_dialog("app_quickaccess"))  
