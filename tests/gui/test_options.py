from dotplot.gui.options import OptionPanel
from dotplot.gui.options import WindowSize
from dotplot.gui.options import Stringency
from dotplot.gui.options import ShowSequence
from dotplot.gui.options import Matrix
from dotplot.gui.helpers import Option
from copy import copy


test_args = {
    'plotter': {
        'window_size': 1,
        'stringency': 4,
        'matrix': None
    },
    'drawer': {
        'show_sequences': 200
    }
}


class DummyNestedNamespace:

    def __init__(self, data):
        data = copy(data)
        for key, value in data.items():
            if type(value) is dict:
                data[key] = DummyNestedNamespace(value)
        self.data = data

    def __getattr__(self, name):
        namespace = self.data
        keys = name.split('.')
        value = namespace[keys[0]]
        if len(keys) > 1 and keys[1]:
            return getattr(value, '.'.join(keys[1:]))
        return value


def test_option_panel(qtbot):

    panel = OptionPanel(DummyNestedNamespace(test_args))

    qtbot.addWidget(panel)

    # check if desired options where automatically added to the panel
    options_expected_in_panel = [
        Matrix,
        WindowSize,
        Stringency,
        ShowSequence
    ]
    options_in_panel = []

    for widget in panel.option_widgets:
        if type(widget) in options_expected_in_panel:
            options_in_panel.append(type(widget))

    assert set(options_expected_in_panel) == set(options_in_panel)


def test_option(qtbot):

    # check if we can declare and create options
    class NullOption(Option):
        name = ''
        target = 'x'

    option = NullOption(DummyNestedNamespace({'x': 0}))

    assert option

    # check if registration of option classes works properly
    class AnotherOption(Option):
        name = ''
        target = 'y'

    # has both option classes (widgets) been registered?
    assert all(
        option in Option.register
        for option in (NullOption, AnotherOption)
    )


def test_window_size(qtbot):

    args = DummyNestedNamespace(test_args)

    window_size_option = WindowSize(args)

    # check if manual value setting works
    window_size_option.value = 5
    assert args.plotter.window_size == 5

    # check if event handling changes value too
    window_size_option.spinner.setValue(10)
    assert args.plotter.window_size == 10

    # make sure that values greater than zero are enforced
    window_size_option.spinner.setValue(0)
    assert args.plotter.window_size == 1

    # let's check if we can add the widget without errors
    qtbot.addWidget(window_size_option)
    assert True


def test_stringency(qtbot):

    raw_args = copy(test_args)

    raw_args['plotter']['window_size'] = 2
    raw_args['plotter']['stringency'] = 1

    args = DummyNestedNamespace(raw_args)

    stringency_option = Stringency(args)

    # make sure that values greater window_size squared are trimmed
    stringency_option.spinner.setValue(10)
    assert args.plotter.stringency == 4

    # check if we can add the widget without errors
    qtbot.addWidget(stringency_option)
    assert True


def test_matrix(qtbot):

    args = DummyNestedNamespace(test_args)

    matrix_option = Matrix(args)

    # check changing value in combo changes arguments value:
    qtbot.keyClicks(matrix_option.combo, 'PAM120')
    assert args.plotter.matrix == 'PAM120'
