from PyQt5.QtWidgets import QMessageBox, QFileDialog

from dotplot.gui.chooser import Chooser
from dotplot.gui.main_window import MainWindow, SequenceSelector
from dotplot.sequence import Sequence
from tests.miscellaneous import DummyNestedNamespace, create_named_temp_file

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
    'parsed_sequences': [None, None]
}


def prepare_test_window(qtbot):
    args = DummyNestedNamespace(test_args)
    window = MainWindow(args)
    qtbot.addWidget(window)
    return window


def add_test_sequences(window):

    window.sequences[0] = Sequence('ABCD', 'test_1')
    window.sequences[1] = Sequence('CDBA', 'test_2')


def test_new_plot(qtbot, mock):
    mock.patch.object(QMessageBox, 'information')
    window = prepare_test_window(qtbot)

    # at the beginning when we have no sequences, the plot should not be created
    success = window.new_plot()
    assert not success

    add_test_sequences(window)

    success = window.new_plot()
    assert success


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
    assert not window.are_sequences_loaded()


def test_set_status(qtbot):

    window = prepare_test_window(qtbot)

    test_message = 'This is a test'
    window.set_status(test_message)
    assert window.statusBar().currentMessage() == test_message


def test_sequence_selector(qtbot, mock):

    window = prepare_test_window(qtbot)
    selector = SequenceSelector(window, 1)

    mock.patch.object(Chooser, 'choose', return_value=('ncbi', 'NP_001009852'))

    selector.callback_more()

    assert window.sequences[0].name == 'NP_001009852.1 bladder cancer-associated protein [Felis catus]'

    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('1.fa', 'txt'))

    selector.callback_file()
    assert window.sequences[0].name == 'Name of sequence 1'
    assert window.sequences[0].sequence == 'AGTTCTAACGTAAAA'

    file_name = create_named_temp_file(suffix='.xxx')

    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(file_name, 'txt'))
    selector.callback_file()

    assert window.statusBar().currentMessage() == (
        'Unknown file extension "xxx" (of file "%s")'
        %
        file_name
    )


def test_save(qtbot, mock):
    import os.path
    window = prepare_test_window(qtbot)
    mock.patch.object(QFileDialog, 'getSaveFileName', return_value=('plot.png', 'PNG file (*.png)'))
    window.select_save_file_dialog()
    assert os.path.exists('plot.png')
