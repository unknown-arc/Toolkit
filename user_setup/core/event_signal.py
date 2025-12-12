from PySide6.QtCore import QObject, Signal

class PageNavigationSignal(QObject):

    back_sgl = Signal()
    next_sgl = Signal()
    continue_sgl = Signal()

    switch_page1 = Signal()
    switch_page2 = Signal()
    switch_page3 = Signal() 
    
class AuthenticationSignal(QObject):  

    show_login_page = Signal()
    show_signup_page = Signal()
        
    login_sgl = Signal() 
    signup_sgl = Signal() 
    guest_log_sgl = Signal()

    login_via_gmail_sgl = Signal() 
    login_via_apple_sgl = Signal()
    login_via_github_sgl = Signal() 
    login_via_outlook_sgl = Signal()

page_nav_sgl = PageNavigationSignal()
auth_sgl = AuthenticationSignal()

# auth_sgl.guest_log_sgl.connect(lambda: print("DEBUG: guest_log_sgl emitted!"))