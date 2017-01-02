from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QComboBox
from .helpers import Option
from .helpers import event


class Spinner(Option):
    """Helper class defining spinner widget to be used together with Option."""

    minimum = 1
    maximum = 10

    def __init__(self, args):
        super().__init__(args)

        spinner = QSpinBox()
        spinner.setMinimum(self.minimum)
        spinner.setMaximum(self.maximum)

        # Note: pylint cannot integrate well with qt
        spinner.valueChanged[int].connect(event(self, 'on_change'))
        self.spinner = spinner
        self.internal_layout.addWidget(spinner)


class WindowSize(Spinner):

    name = 'Window size'
    target = 'plotter.window_size'
    maximum = 1000

    def __init__(self, args):
        super().__init__(args)
        self.update()

    def update(self):
        self.spinner.setValue(self.value)

    def on_change(self, value):
        self.value = value


class Stringency(Spinner):

    name = 'Stringency'
    target = 'plotter.stringency'
    minimum = 0
    maximum = 1000

    def __init__(self, args):
        super().__init__(args)
        self.update()

    def update(self):
        value = 0 if self.value is None else self.value
        self.spinner.setValue(value)

    def on_change(self, value):

        maximum = pow(self.args.plotter.window_size, 2)

        if value > maximum:
            self.value = maximum
            self.update()
        else:
            if value == 0:
                value = None
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
        self.internal_layout.addWidget(combo)
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

        self.option_widgets = []

        # Note: pylint cannot understand magic of metaclasses
        for option_constructor in Option.register:
            option = option_constructor(args)
            self.addWidget(option)
            self.option_widgets.append(option)
