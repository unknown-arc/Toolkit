from PySide6.QtWidgets import QStackedWidget

from gui.main_window.main_page import MainWindowPage
from gui.app_setting.settings_page import SettingsPage
from gui.market_place.marketplace_page import MarketPlacePage
from core.signal_manager import Header_eb


class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.pages = {}

        # Create all pages here
        self.main_page = MainWindowPage()
        self.settings_page = SettingsPage()
        self.marketplace_page = MarketPlacePage()  # Placeholder for MarketplacePage

        # Add to the manager
        self.add_page("main", self.main_page)
        self.add_page("settings", self.settings_page)
        self.add_page("marketplace", self.marketplace_page)  # Placeholder 

        # Connect Open signals
        Header_eb.open_settings_page.connect(lambda: self.show_page("settings"))
        Header_eb.open_marketplace_page.connect(lambda: self.show_page("marketplace"))

        # Connect Back signal
        Header_eb.back_to_main_page.connect(lambda: self.show_page("main"))
    

    def add_page(self, name: str, widget):
        self.pages[name] = widget
        self.addWidget(widget)

    def show_page(self, name: str):
        if name in self.pages:
            self.setCurrentWidget(self.pages[name])
        else:
            print(f"Page '{name}' not found")


