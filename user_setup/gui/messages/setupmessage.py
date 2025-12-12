from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class FormMessage(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Hi"))

class OccupationMessage(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("What's your occupation"))        

class AppearanceMessage(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Choose your appearance settings"))

             

        