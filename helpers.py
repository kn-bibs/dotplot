from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel


class Register(type):
    """Metaclass used to register all leaves-classes in hierarchy."""

    def __init__(cls, name, bases, attrs):

        super().__init__(name, bases, attrs)

        if not hasattr(cls, 'register'):
            cls.register = set()

        cls.register.add(cls)
        cls.register -= set(bases)


class Option(metaclass=Register):
    """An abstract class for convenient creation and registration of options."""

    def __init__(self, args):
        self.args = args
        self.label = QLabel(self.name)
        self.inner_layout = QVBoxLayout()
        self.inner_layout.addWidget(self.label)
        self.exposed_layout = QVBoxLayout()
        self.inner_layout.addLayout(self.exposed_layout)
        self.widget = QWidget()
        self.widget.setLayout(self.inner_layout)
        self.target_path = self.target.split('.')
        self.layout = self.exposed_layout

    @property
    def name(self):
        """A display name (label) for given option to be shown in GUI."""
        raise NotImplementedError

    @property
    def target(self):
        """Dot-separated string representing place in arguments namespace,
        where an argument which will be modified by the option is stored."""
        raise NotImplementedError

    @property
    def value(self):
        """Getter for the argument targeted by the option."""
        args = self.args
        for name in self.target_path:
            args = getattr(args, name)
        return args

    @value.setter
    def value(self, value):
        """Setter for the argument targeted by the option."""
        args = self.args
        for name in self.target_path[:-1]:
            args = getattr(args, name)
        setattr(args, self.target_path[-1], value)


def event(self, name):
    """This is a big fake. Long story short: this function stays here.

    It is not normal to generate dummy closures just to get an address of a
    method. But PyQt5 has to have a function, not a method given for sake of
    setting a connection successfuly; it is because QObject cannot be used with
    a metaclass and one is already used to register options.
    """
    method = getattr(self, name)

    def closure(*args, **kwargs):
        method(*args, **kwargs)

    return closure
