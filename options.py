from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSplitter


class Register(type):

    def __init__(cls, name, bases, attrs):

        super().__init__(name, bases, attrs)

        if not hasattr(cls, 'register'):
            cls.register = set()

        cls.register.add(cls)
        cls.register -= set(bases)


class Option(metaclass=Register):

    def __init__(self, controls_layout):

        label = QLabel(self.name)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(controls_layout)
        self.widget = QWidget()
        self.widget.setLayout(layout)

    @property
    def name(self):
        return NotImplementedError


class WindowSize(Option):

    name = 'Window size'

    def __init__(self, args):

        value = args.plotter.window_size

        btn = QPushButton(value)
        vbox = QVBoxLayout()
        vbox.addWidget(btn)

        super().__init__(vbox)


class OptionPanel(QVBoxLayout):

    def __init__(self, args):
        super().__init__()

        for option_constructor in Option.register:
            option = option_constructor(args)
            self.addWidget(option.widget)
