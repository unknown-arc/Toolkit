from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QFrame, QVBoxLayout
from PySide6.QtCore import Qt

class DetailsCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Right card styling
        self.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA; /* Off-white background for detail container */
                border-radius: 12px;
                padding: 25px;
                border: 1px solid #EAEAEA;
            }
        """)
        
        v_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        # Helper function for label text
        def create_label(text):
            label = QLabel(text)
            label.setStyleSheet("font-size: 14px; color: #7F8C8D; font-weight: 500;")
            return label

        # Helper function for the professional input fields
        def create_value_widget():
            line_edit = QLineEdit()
            line_edit.setReadOnly(True) 
            line_edit.setObjectName("DetailValue")
            line_edit.setStyleSheet("""
                QLineEdit#DetailValue {
                    border: 1px solid #DCE4EC;
                    border-radius: 6px;
                    padding: 8px 10px;
                    background-color: white; /* Crisp white input field */
                    font-size: 16px;
                    color: #2C3E50;
                }
            """)
            return line_edit
        
        # --- Detail Fields ---
        
        self.name_value = create_value_widget()
        form_layout.addRow(create_label("FULL NAME"), self.name_value)
        
        self.gender_value = create_value_widget()
        form_layout.addRow(create_label("GENDER"), self.gender_value)
        
        self.age_value = create_value_widget()
        form_layout.addRow(create_label("AGE"), self.age_value)
        
        self.email_value = create_value_widget()
        form_layout.addRow(create_label("EMAIL ADDRESS"), self.email_value)
        
        v_layout.addLayout(form_layout)
        v_layout.addStretch()

    def update_values(self, data):
        self.name_value.setText(data.get("name", ""))
        self.gender_value.setText(data.get("gender", ""))
        self.age_value.setText(data.get("age", ""))
        self.email_value.setText(data.get("email", ""))