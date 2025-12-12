from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QApplication, QSizePolicy, QPushButton, QLabel, QButtonGroup, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor


import sys

class OccupationSelection(QWidget):
    """Occupation selection with 2x2 grid layout."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- Main vertical layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # --- Question label ---
        question_label = QLabel("Please select your current occupation:")
        question_label.setFont(QFont("Segoe UI", 13))
        main_layout.addWidget(question_label, alignment=Qt.AlignLeft)

        # --- Options grid (2x2) ---
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        option_names = ["Student", "Teacher", "Working Professional", "Other"]
        self.option_buttons = []
        self.option_group = QButtonGroup(self)

        for idx, name in enumerate(option_names):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedSize(160, 60)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #dcdcdc;
                    border-radius: 12px;
                    background-color: #ffffff;
                    font-family: 'Segoe UI';
                    font-size: 14px;
                }
                QPushButton:checked {
                    border: 3px solid #0078D7;
                }
            """)
            self.option_group.addButton(btn)
            self.option_buttons.append(btn)
            row, col = divmod(idx, 2)  # 2 columns
            grid_layout.addWidget(btn, row, col)

        main_layout.addLayout(grid_layout)

    def get_selected_option(self):
        """Return the selected occupation, or None."""
        for btn in self.option_buttons:
            if btn.isChecked():
                return btn.text()
        return None


# # --- Preview ---
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     window = OccupationSelection()
#     window.resize(600, 200)
#     window.show()
#     sys.exit(app.exec())
