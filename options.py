from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QComboBox
from helpers import Option
from helpers import event


class WindowSize(Option):

    name = 'Window size'
    target = 'plotter.window_size'

    def __init__(self, args):
        super().__init__(args)

        spinner = QSpinBox()
        spinner.setMinimum(1)
        spinner.setMaximum(1000)

        # Note: pylint cannot integrate well with qt
        spinner.valueChanged[int].connect(event(self, 'on_change'))
        self.spinner = spinner
        self.layout.addWidget(spinner)

        self.update()

    def update(self):
        self.spinner.setValue(self.value)

    def on_change(self, value):
        self.value = value


class Matrix(Option):

    name = 'Similarity matrix'
    target = 'plotter.matrix'
    choices = ['PAM120', 'None']

    def __init__(self, args):
        super().__init__(args)

        combo = QComboBox()
        combo.addItems(self.choices)
        combo.activated[str].connect(event(self, 'on_change'))
        self.combo = combo
        self.layout.addWidget(combo)
        self.update()

    def update(self):
        self.combo.setCurrentText(str(self.value))

    def on_change(self, value):
        if value == 'None':
            value = None
        self.value = value


class OptionPanel(QVBoxLayout):
    """Layout containing option widgets.

    It reflects changes specified by the user directly in the given `args`
    object (which is expected to be a NestedNamespace).
    """

    def __init__(self, args):
        super().__init__()
        self.setAlignment(Qt.AlignTop)

        # Note: pylint cannot understand magic of metaclasses
        for option_constructor in Option.register:
            option = option_constructor(args)
            self.addWidget(option.widget)
