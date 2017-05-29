from PyQt5 import QtCore

from dotplot.gui.chooser import Chooser


def test_chooser(qtbot):
    chooser = Chooser(default_db='ncbi')
    qtbot.addWidget(chooser)

    active_option = chooser.databases['ncbi']

    assert active_option.button.isChecked()
    assert chooser.id_input.placeholderText() == 'example: ' + active_option.example
    assert chooser.id_input.text() == ''

    # text example loading
    qtbot.mouseClick(chooser.example_button, QtCore.Qt.LeftButton)
    assert chooser.id_input.text() == active_option.example

    # test selection switching
    new_option = chooser.databases['uniprot']
    qtbot.mouseClick(new_option.button, QtCore.Qt.LeftButton)
    assert new_option.button.isChecked()

    # make sure that example has changed
    assert chooser.id_input.placeholderText() == 'example: ' + new_option.example

    # and that example button has new signal connected
    qtbot.mouseClick(chooser.example_button, QtCore.Qt.LeftButton)
    assert chooser.id_input.text() == new_option.example
