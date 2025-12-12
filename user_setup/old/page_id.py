from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette


class PageTracker(QWidget):
    """
    Step tracker widget.
    - total_steps: number of steps
    - current_step: current page id
    - completed_steps: list of completed page ids
    """
    def __init__(self, total_steps=3, current_step=1, completed_steps=None, parent=None):
        super().__init__(parent)
        if completed_steps is None:
            completed_steps = []

        self.total_steps = total_steps
        self.current_step = current_step
        self.completed_steps = completed_steps

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(12)
        self.layout.setAlignment(Qt.AlignHCenter)
        self.steps = []

        self._build_steps()

    def _build_steps(self):
        for i in range(1, self.total_steps + 1):
            lbl = QLabel(f"Step {i}")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(100, 40)
            lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            lbl.setStyleSheet(self._get_style(i))
            self.layout.addWidget(lbl)
            self.steps.append(lbl)

    def _get_style(self, step_id):
        """Return style for a step based on its state."""
        if step_id == self.current_step:
            # Current step: black fill
            return """
                QLabel {
                    background-color: #000000;
                    color: #ffffff;
                    border-radius: 20px;
                    padding: 6px 12px;
                }
            """
        elif step_id in self.completed_steps:
            # Completed step: green fill
            return """
                QLabel {
                    background-color: #28a745;
                    color: #ffffff;
                    border-radius: 20px;
                    padding: 6px 12px;
                }
            """
        else:
            # Pending step: hollow
            return """
                QLabel {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 20px;
                    padding: 6px 12px;
                }
            """

    def set_current_step(self, step_id):
        """Set which step is current and update styles."""
        self.current_step = step_id
        self._update_styles()

    def set_completed_steps(self, completed_list):
        """Set completed steps and update styles."""
        self.completed_steps = completed_list
        self._update_styles()

    def _update_styles(self):
        for i, lbl in enumerate(self.steps, start=1):
            lbl.setStyleSheet(self._get_style(i))

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout(window)

    step_tracker = PageTracker(total_steps=4, current_step=2, completed_steps=[1])
    layout.addWidget(step_tracker)

    window.show()
    app.exec()