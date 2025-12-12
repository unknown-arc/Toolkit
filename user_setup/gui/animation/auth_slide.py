from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

def slide_transition(left_widget: QWidget, right_widget: QWidget,
                     new_left: QWidget, new_right: QWidget,
                     duration=500):
    """
    Animate a transition between old and new left/right widgets.
    The content slides to its new side, and the message appears.
    """
    # Geometry
    left_geo = left_widget.geometry()
    right_geo = right_widget.geometry()

    # Animate old widgets sliding out
    anim_old_left = QPropertyAnimation(left_widget, b"geometry")
    anim_old_left.setDuration(duration // 2)
    anim_old_left.setStartValue(left_geo)
    anim_old_left.setEndValue(left_geo.translated(-left_geo.width(), 0))
    anim_old_left.setEasingCurve(QEasingCurve.InOutQuad)

    anim_old_right = QPropertyAnimation(right_widget, b"geometry")
    anim_old_right.setDuration(duration // 2)
    anim_old_right.setStartValue(right_geo)
    anim_old_right.setEndValue(right_geo.translated(right_geo.width(), 0))
    anim_old_right.setEasingCurve(QEasingCurve.InOutQuad)

    # After old widgets are gone, replace with new widgets
    def on_old_finished():
        parent = left_widget.parentWidget()
        # Remove old widgets
        left_widget.setParent(None)
        right_widget.setParent(None)

        # Add new widgets off-screen
        new_left.setParent(parent)
        new_right.setParent(parent)

        new_left.setGeometry(left_geo.translated(-left_geo.width(), 0))
        new_right.setGeometry(right_geo.translated(right_geo.width(), 0))

        # Animate new widgets sliding in
        anim_new_left = QPropertyAnimation(new_left, b"geometry")
        anim_new_left.setDuration(duration // 2)
        anim_new_left.setStartValue(new_left.geometry())
        anim_new_left.setEndValue(left_geo)
        anim_new_left.setEasingCurve(QEasingCurve.OutCubic)

        anim_new_right = QPropertyAnimation(new_right, b"geometry")
        anim_new_right.setDuration(duration // 2)
        anim_new_right.setStartValue(new_right.geometry())
        anim_new_right.setEndValue(right_geo)
        anim_new_right.setEasingCurve(QEasingCurve.OutCubic)

        group_new = QParallelAnimationGroup()
        group_new.addAnimation(anim_new_left)
        group_new.addAnimation(anim_new_right)
        group_new.start()

    group_old = QParallelAnimationGroup()
    group_old.addAnimation(anim_old_left)
    group_old.addAnimation(anim_old_right)
    group_old.finished.connect(on_old_finished)
    group_old.start()
