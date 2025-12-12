from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QSize
import sys

from gui.market_place.navbar import NavBar
from gui.market_place.content_frame import ContentFrame
from gui.market_place.contents.home_page import HomePage
from gui.market_place.contents.explore_page import ExplorePage
from gui.market_place.contents.apps_page import AppsPage 
from gui.market_place.contents.installedapps_page import InstalledPage

from core.signal_manager import marketplace_eb
class MarketplaceManager:
    def __init__(self):
        # pages
        self.stacked = QStackedWidget()
        self.pages = {
            "Home": HomePage(),
            "Explore": ExplorePage(),
            "Apps": AppsPage(),
            "Installed": InstalledPage()
        }

        for p in self.pages.values():
            self.stacked.addWidget(p)

        # navbar
        self.nav_bar = NavBar()

        # final ContentFrame containing navbar + pages
        self.content_frame = ContentFrame(
            nav_bar_widget=self.nav_bar,
            stacked_widget=self.stacked
        )

        marketplace_eb.nav_selection_page.connect(self._change_page)
        self._change_page("Home")

    def _change_page(self, name):
        if name in self.pages:
            self.stacked.setCurrentWidget(self.pages[name])
        else:
            print("Page not found:", name)
