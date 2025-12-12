from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MultiStageStepTracker(QWidget):
    """
    Step tracker widget with multiple states per step.
    - total_steps: number of steps
    - step_states: list of 5-stage values per step
    """

    # Define possible states
    STATE_UNFILLED = 1
    STATE_GREEN_FILL = 2
    STATE_GREEN_FILL2 = 3
    STATE_GREEN_BORDER_FILL = 4
    STATE_RED_BORDER_FILL = 5

    def __init__(self, total_steps=3, step_states=None, parent=None):
        super().__init__(parent)
        self.total_steps = total_steps
        if step_states is None:
            # default: all steps unfilled
            step_states = [self.STATE_UNFILLED] * total_steps
        self.step_states = step_states

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignHCenter)
        self.steps = []

        self._build_steps()

    def _build_steps(self):
        """Create labels for each step and apply initial styles."""
        for i in range(1, self.total_steps + 1):
            lbl = QLabel(f"Step {i}")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(100, 40)
            lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            lbl.setStyleSheet(self._get_style(self.step_states[i - 1]))
            self.layout.addWidget(lbl)
            self.steps.append(lbl)

    def _get_style(self, state):
        """Return stylesheet for a given step state."""
        border_size = "4px"  # Increased border
        if state == self.STATE_UNFILLED:
            return f"""
                QLabel {{
                    background-color: #ffffff;
                    color: #000000;
                    border: {border_size} solid #000000;
                    border-radius: 20px;
                    padding: 6px 12px;
                }}
            """
        elif state in (self.STATE_GREEN_FILL, self.STATE_GREEN_FILL2):
            return """
                QLabel {
                    background-color: #28a745;
                    color: #ffffff;
                    border-radius: 20px;
                    padding: 6px 12px;
                }
            """
        elif state == self.STATE_GREEN_BORDER_FILL:
            return f"""
                QLabel {{
                    background-color: #28a745;
                    color: #ffffff;
                    border: {border_size} solid #000000;
                    border-radius: 20px;
                    padding: 6px 12px;
                }}
            """
        elif state == self.STATE_RED_BORDER_FILL:
            return f"""
                QLabel {{
                    background-color: #dc3545;
                    color: #ffffff;
                    border: {border_size} solid #000000;
                    border-radius: 20px;
                    padding: 6px 12px;
                }}
            """
        else:
            # fallback
            return f"""
                QLabel {{
                    background-color: #ffffff;
                    color: #000000;
                    border: {border_size} solid #000000;
                    border-radius: 20px;
                    padding: 6px 12px;
                }}
            """

    def set_step_state(self, step_id, state):
        """Update a specific step state."""
        if 1 <= step_id <= self.total_steps:
            self.step_states[step_id - 1] = state
            self.steps[step_id - 1].setStyleSheet(self._get_style(state))

    def set_all_states(self, states_list):
        """Update all step states at once."""
        for idx, state in enumerate(states_list):
            if idx < self.total_steps:
                self.step_states[idx] = state
                self.steps[idx].setStyleSheet(self._get_style(state))


# ---------------- Preview ----------------
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout(window)

    # Example: 3 steps with different stage types
    step_tracker = MultiStageStepTracker(
        total_steps=3,
        step_states=[
            MultiStageStepTracker.STATE_UNFILLED,
            MultiStageStepTracker.STATE_GREEN_FILL,
            MultiStageStepTracker.STATE_RED_BORDER_FILL
        ]
    )
    layout.addWidget(step_tracker)

    window.resize(400, 100)
    window.show()
    app.exec()
