from core.event_signal import auth_sgl


auth_sgl.guest_login_sgl.connect(lambda: print("DEBUG: guest_login_sgl emitted!"))