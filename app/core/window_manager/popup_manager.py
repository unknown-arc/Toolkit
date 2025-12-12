# popup_manager.py
from gui.popups.app_notifications.notification_popup import NotificationPopup
from core.signal_manager import Header_eb



class PopupManager:
    def __init__(self, parent):
        self.parent = parent
        self.popups = {}

        self.add_popups()
        self.connect_signals()

    def add_popups(self):
        self.register_popup("notifications", NotificationPopup)

    def register_popup(self, name: str, popup_class):
        self.popups[name] = popup_class

    def connect_signals(self):
        Header_eb.open_notification_popup.connect(
            lambda btn: self.show_popup("notifications", btn)
        )

    def show_popup(self, name, btn):
        popup_class = self.popups.get(name)
        if not popup_class:
            return
        popup = popup_class(self.parent)
        popup.show_below(btn)
