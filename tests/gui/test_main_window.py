from PyQt5.QtWidgets import QMessageBox

from dotplot.gui.main_window import MainWindow
from tests.gui.miscellaneous import DummyNestedNamespace


test_args = {
    'plotter': {
        'window_size': 1,
        'stringency': 4,
        'matrix': None
    },
    'drawer': {
        'show_sequences': 200,
        'method': 'matplotlib'
    },
    'parsed_sequences': []
}


def prepare_test_window(qtbot):
    args = DummyNestedNamespace(test_args)
    window = MainWindow(args)
    qtbot.addWidget(window)
    return window


def test_new_plot(qtbot, mock):
    mock.patch.object(QMessageBox, 'information')
    window = prepare_test_window(qtbot)

    # at the beginning when we have no sequences, the plot should not be created
    success = window.new_plot()
    assert not success


def test_about(qtbot, mock):
    mock.patch.object(QMessageBox, 'about')

    window = prepare_test_window(qtbot)
    window.about()


def test_tutorial(qtbot, mock):
    mock.patch.object(QMessageBox, 'about')

    window = prepare_test_window(qtbot)
    window.tutorial()


def test_sequences_load(qtbot):

    window = prepare_test_window(qtbot)
    assert window.are_sequences_loaded() is False


def test_set_status(qtbot):

    window = prepare_test_window(qtbot)

    test_message = 'It is a test'
    window.set_status(test_message)
    assert window.statusBar().currentMessage() == test_message
