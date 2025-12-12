# shake.py
from PySide6.QtCore import QPropertyAnimation, QPoint

# Animate widget position around its original pos.
# We return the animation so caller can keep a reference if desired.
def shake_widget(widget, distance=8, duration=300):
    # Make sure widget has a parent (we animate absolute pos relative to parent)
    parent = widget.parent()
    if parent is None:
        return None

    anim = QPropertyAnimation(widget, b"pos", parent)
    original = widget.pos()
    anim.setDuration(duration)

    # keyframes: start, left, right, left, original
    anim.setKeyValueAt(0.0, original)
    anim.setKeyValueAt(0.10, original + QPoint(-distance, 0))
    anim.setKeyValueAt(0.30, original + QPoint(distance, 0))
    anim.setKeyValueAt(0.50, original + QPoint(-distance, 0))
    anim.setKeyValueAt(0.70, original + QPoint(distance, 0))
    anim.setKeyValueAt(1.0, original)

    anim.start()
    return anim
