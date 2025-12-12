from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QComboBox, QFrame, QGraphicsDropShadowEffect, QButtonGroup
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor, QColor

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QApplication, QSizePolicy, QPushButton, QLabel, QButtonGroup, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

class UserInfoForm(QWidget):
    """User setup page 1 – Basic Info"""
    continue_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # === Outer Layout ===
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(25)
        main_layout.setAlignment(Qt.AlignCenter)

        # === Form Layout ===
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        # --- Full Name ---
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self._style_input(self.name_input)

        # --- Date of Birth ---
        dob_layout = QHBoxLayout()
        dob_layout.setSpacing(8)
        self.day_combo = QComboBox()
        self.month_combo = QComboBox()
        self.year_combo = QComboBox()

        for cb, w in zip([self.day_combo, self.month_combo, self.year_combo], [80, 120, 100]):
            cb.setFixedWidth(w)
            cb.setFixedHeight(32)
            cb.setStyleSheet("""
                QComboBox {
                    border: 1.5px solid #dcdcdc;
                    border-radius: 8px;
                    padding-left: 6px;
                    font-size: 13px;
                    background: #fff;
                }
                QComboBox::drop-down { width: 20px; }
            """)

        self.day_combo.addItem("Day")
        for i in range(1, 32):
            self.day_combo.addItem(str(i))

        self.month_combo.addItems([
            "Month", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ])
 
        self.year_combo.addItem("Year")
        for year in range(1950, 2025):
            self.year_combo.addItem(str(year))

        dob_layout.addWidget(self.day_combo)
        dob_layout.addWidget(self.month_combo)
        dob_layout.addWidget(self.year_combo)

        # --- Gender Buttons ---
        gender_layout = QHBoxLayout()
        gender_layout.setSpacing(10)

        self.male_btn = QPushButton("Male")
        self.female_btn = QPushButton("Female")
        self.other_btn = QPushButton("Other")

        for btn in [self.male_btn, self.female_btn, self.other_btn]:
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedWidth(90)
            btn.setFixedHeight(34)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #dcdcdc;
                    border-radius: 8px;
                    background-color: #ffffff;
                    font-size: 13px;
                }
                QPushButton:checked {
                    color: white;
                }
            """)

        self.male_btn.setStyleSheet(self.male_btn.styleSheet() + """
            QPushButton { border: 2px solid #0078D7; }
            QPushButton:checked { background-color: #0078D7; }
        """)
        self.female_btn.setStyleSheet(self.female_btn.styleSheet() + """
            QPushButton { border: 2px solid #E91E63; }
            QPushButton:checked { background-color: #E91E63; }
        """)
        self.other_btn.setStyleSheet(self.other_btn.styleSheet() + """
            QPushButton { border: 2px solid #9E9E9E; }
            QPushButton:checked { background-color: #9E9E9E; }
        """)

        # Gender group
        from PySide6.QtWidgets import QButtonGroup
        gender_group = QButtonGroup(self)
        gender_group.addButton(self.male_btn)
        gender_group.addButton(self.female_btn)
        gender_group.addButton(self.other_btn)

        gender_layout.addWidget(self.male_btn)
        gender_layout.addWidget(self.female_btn)
        gender_layout.addWidget(self.other_btn)

        # --- Email & Phone ---
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email (optional)")
        self._style_input(self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number (optional)")
        self._style_input(self.phone_input)

        # Add form rows
        form_layout.addRow("Full Name:", self.name_input)
        form_layout.addRow("Date of Birth:", dob_layout)
        form_layout.addRow("Gender:", gender_layout)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)

        main_layout.addLayout(form_layout)

    def _style_input(self, widget):
        widget.setFixedHeight(34)
        widget.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #dcdcdc;
                border-radius: 8px;
                padding-left: 8px;
                font-size: 13px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 1.5px solid #000000;
            }
        """)

    def get_user_info(self):
        gender = ""
        if self.male_btn.isChecked():
            gender = "Male"
        elif self.female_btn.isChecked():
            gender = "Female"
        elif self.other_btn.isChecked():
            gender = "Other"

        return {
            "name": self.name_input.text(),
            "dob": f"{self.day_combo.currentText()} {self.month_combo.currentText()} {self.year_combo.currentText()}",
            "gender": gender,
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
        }
