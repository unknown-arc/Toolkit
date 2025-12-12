from PySide6.QtWidgets import (
    QWidget, QLineEdit, QComboBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QButtonGroup, QApplication
)
from PySide6.QtCore import Qt, Signal
import sys


class UserInfoForm(QWidget):
    continue_clicked = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(6)

        # --------------------------
        # Styles
        # --------------------------
        input_style = """
            QLineEdit {
                background: white;
                border: 1px solid #C9C9C9;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """

        combo_style = """
            QComboBox {
                background: white;
                border: 1px solid #C9C9C9;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #333;
                min-width: 80px;
            }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox QAbstractItemView {
                background: white;
                color: #333;
                selection-background-color: #4A90E2;
                selection-color: white;
            }
        """

        gender_button_style = """
            QPushButton {
                border-radius: 8px;
                border: 2px solid #C9C9C9;
                background-color: white;
                font-size: 14px;
            }
            QPushButton:checked { color: white; }
        """

        # --------------------------
        # 1. Name Section
        # --------------------------
        fname = QLineEdit()
        lname = QLineEdit()
        fname.setPlaceholderText("First Name")
        lname.setPlaceholderText("Last Name")
        fname.setStyleSheet(input_style)
        lname.setStyleSheet(input_style)
        fname.setAlignment(Qt.AlignLeft)
        lname.setAlignment(Qt.AlignLeft)

        name_layout = QHBoxLayout()
        name_layout.setSpacing(10)
        name_layout.addWidget(fname)
        name_layout.addWidget(lname)


        # --------------------------
        # 2. Gender Section (Modern)
        # --------------------------
        

        self.male_btn = QPushButton("Male")
        self.female_btn = QPushButton("Female")
        self.other_btn = QPushButton("Other")

        for btn in [self.male_btn, self.female_btn, self.other_btn]:
            btn.setCheckable(True)
            btn.setStyleSheet(gender_button_style)
            btn.setFixedHeight(36)

        # Equal widths
        self.male_btn.setFixedWidth(100)
        self.female_btn.setFixedWidth(100)
        self.other_btn.setFixedWidth(100)

        # Checked styles with colors
        self.male_btn.setStyleSheet(self.male_btn.styleSheet() + """
            QPushButton:checked { background-color: #0078D7; border: 2px solid #0078D7; }
        """)
        self.female_btn.setStyleSheet(self.female_btn.styleSheet() + """
            QPushButton:checked { background-color: #E91E63; border: 2px solid #E91E63; }
        """)
        self.other_btn.setStyleSheet(self.other_btn.styleSheet() + """
            QPushButton:checked { background-color: #9E9E9E; border: 2px solid #9E9E9E; }
        """)

        # Group (mutually exclusive)
        gender_group = QButtonGroup(self)
        gender_group.setExclusive(True)
        gender_group.addButton(self.male_btn)
        gender_group.addButton(self.female_btn)
        gender_group.addButton(self.other_btn)

        gender_layout = QHBoxLayout()
        gender_layout.setSpacing(10)
        gender_layout.addWidget(self.male_btn)
        gender_layout.addWidget(self.female_btn)
        gender_layout.addWidget(self.other_btn)


        # --------------------------
        # 3. DOB Section
        # --------------------------
        dob_layout = QHBoxLayout()
        dob_layout.setSpacing(10)

        day = QComboBox()
        month = QComboBox()
        year = QComboBox()

        day.addItems([f"{i:02d}" for i in range(1, 32)])
        month.addItems(["Jan","Feb","Mar","Apr","May","Jun",
                        "Jul","Aug","Sep","Oct","Nov","Dec"])
        year.addItems([str(i) for i in range(1980, 2025)])

        day.setStyleSheet(combo_style)
        month.setStyleSheet(combo_style)
        year.setStyleSheet(combo_style)

        dob_layout.addWidget(day)
        dob_layout.addWidget(month)
        dob_layout.addWidget(year)

        # --------------------------
        # 4. Email Section
        # --------------------------
        email = QLineEdit()
        email.setPlaceholderText("Enter your email")
        email.setStyleSheet(input_style)
        email.setClearButtonEnabled(True)
        email.setAlignment(Qt.AlignLeft)

        # ---Layout---
        layout.addLayout(name_layout)
        layout.addLayout(dob_layout)
        layout.addLayout(gender_layout)
        layout.addWidget(email)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UserInfoForm()
    w.setStyleSheet("background: #F3F3F3;")
    w.resize(500, 400)
    w.show()
    sys.exit(app.exec())
