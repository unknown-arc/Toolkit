from PySide6.QtCore import QObject, Signal

class HeaderEventBus(QObject):
    
    # ---Open Signals---
    open_settings_page = Signal()
    open_marketplace_page = Signal()

    open_notification_popup = Signal(object)

    open_gethelp_dialog = Signal()
    open_userprofile_dialog = Signal()

    # ---Back to Main Window Signal---
    back_to_main_page = Signal()
    close_dialog = Signal()
    close_popup = Signal()

    # ---Dropdown Signals---
    toggle_theme_dropdown = Signal()
    toggle_language_dropdown = Signal() 

class QuickaccessEventBus(QObject):

    open_app = Signal(str)
    open_quickaccess_dialog = Signal()
 

class LeftPanelEventBus(QObject):

    new_lab = Signal()
    incognito_lab = Signal(str)
    close_all_labs = Signal()  

class LabEventBus(QObject):

    add_lab = Signal(str)
    close_lab = Signal(str)             
    active_lab = Signal(str) 
    
    rename_lab = Signal(dict) 
    # reorder_labs = Signal(int, int)   
    incognito_lab = Signal(dict)  
    # selected_lab = Signal()

class LabPillEventBus(QObject):

    new_pill = Signal(object)
    add_pill = Signal(object)
    remove_pill = Signal(str)
    remove_all_pills = Signal()
    active_pill = Signal(str)
    rename_pill = Signal(dict)
    reorder_pills = Signal(int, int)
    incognito_pill = Signal(object)



class LabSessionEventBus(QObject):

    add_session = Signal(object)
    close_session = Signal(str)
    active_session = Signal(str)
    rename_session = Signal(dict)
    close_all_sessions = Signal() 

    session_closed = Signal(str)   
    all_sessions_closed = Signal()
    

class SaveFileEventBus(QObject):

    save_session_req = Signal(object)  # file_path, content

class MarketplaceEventBus(QObject):

    nav_selection_page = Signal(str)  # page name


Header_eb = HeaderEventBus()
LeftPanel_eb = LeftPanelEventBus()
Lab_eb = LabEventBus()
Quickaccess_eb = QuickaccessEventBus()
Save_eb = SaveFileEventBus()
marketplace_eb = MarketplaceEventBus()
Session_eb = LabSessionEventBus()
Pill_eb = LabPillEventBus()
