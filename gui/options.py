from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QRadioButton
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


class ShowSequence(Option):

    name = 'Show sequences'
    target = 'drawer.show_sequences'

    def __init__(self, args):
        super().__init__(args)

        self.always = QRadioButton('always', self)
        self.never = QRadioButton('never', self)
        self.seq_lt = QRadioButton('if a sequenece is shorter than', self)

        combo = QComboBox()
        combo.addItems(['100', '200', '500', '1000'])
        combo.setEditable(True)

        self.seq_len_combo = combo

        hbox = QHBoxLayout()
        hbox.addWidget(self.always)
        hbox.addWidget(self.never)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.seq_lt)
        vbox.addWidget(self.seq_len_combo)

        self.internal_layout.addLayout(vbox)

        self.update()

        combo.activated[str].connect(event(self, 'on_change'))
        combo.editTextChanged[str].connect(event(self, 'on_change'))
        self.always.toggled.connect(event(self, 'on_change', 'always'))
        self.never.toggled.connect(event(self, 'on_change', 'never'))
        self.seq_lt.toggled.connect(event(self, 'on_change', 'seq_lt'))

    def on_change(self, given_value, caller_name=None):

        if caller_name == 'seq_lt':
            value = self.seq_len_combo.currentText()
        elif caller_name == 'always':
            value = True
        elif caller_name == 'never':
            value = False
        else:
            if not self.seq_lt.isChecked():
                self.seq_lt.toggle()
            try:
                value = int(given_value)
            except ValueError:
                # TODO add custom exception, show feedback to user
                # TODO also give notice if int is not positive
                print('Invalid value for sequence length')
                return

        self.value = value

    def update(self):

        if type(self.value) is int:
            self.seq_len_combo.setCurrentText(str(self.value))
            self.seq_lt.toggle()
        else:
            value = bool(self.value)
            if value:
                self.always.toggle()
            else:
                self.never.toggle()


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
