# core/external_registry.py

external_widgets = []

def register(widget):
    """Register external app widgets globally."""
    external_widgets.append(widget)

def cleanup():
    """Called when the main app exits to kill all external apps."""
    for w in list(external_widgets):
        try:
            w.force_close()
        except:
            pass
