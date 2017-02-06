from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from sip import wrappertype


class Register(wrappertype):
    """Metaclass used to register all leaves-classes in hierarchy."""

    def __init__(cls, name, bases, attrs):

        super().__init__(name, bases, attrs)

        if not hasattr(cls, 'register'):
            cls.register = set()

        cls.register.add(cls)
        cls.register -= set(bases)


class Option(QWidget, metaclass=Register):
    """An abstract class for convenient creation and registration of options."""

    def __init__(self, args):

        super().__init__()

        # bind a reference to arguments namespace to an Option instance
        self.args = args

        # create a path to the targeted option (a list of subsequent keys to
        # be called in arguments namespace to get or modify targeted argumnet)
        self.target_path = self.target.split('.')

        # will raise ValueError if target is not accessible
        self._check_target()

        # create the GUI for the option widget
        self.container = QVBoxLayout()

        self.label = QLabel(self.name, parent=self)
        self.container.addWidget(self.label)

        # allocate place for option-specific widgets
        self.internal_layout = QVBoxLayout()
        self.container.addLayout(self.internal_layout)

        self.setLayout(self.container)

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

    def _check_target(self):
        """Check if an argument under specified `target` path is accesible."""
        try:
            self.value
        except AttributeError:
            raise ValueError(
                'Initialization of "{name}" failed: cannot find an argument'
                ' specified by target "{target}" in provided args namespace'
                .format(name=self.name, target=self.target)
            )


def event(self, name, caller_name=None):
    """This is a big fake. Long story short: this function stays here.

    It is not normal to generate dummy closures just to get an address of a
    method. But PyQt5 has to have a function, not a method given for sake of
    setting a connection successfuly; it is because QObject cannot be used with
    a metaclass and one is already used to register options.
    """
    method = getattr(self, name)

    def closure(*args, **kwargs):
        if caller_name:
            kwargs['caller_name'] = caller_name

        method(*args, **kwargs)

    return closure
