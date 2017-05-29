from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QLineEdit


def reconnect(signal, handler):
    """Remove existing handlers and connect a new one to given signal"""
    try:
        signal.disconnect()
    except TypeError:
        pass
    signal.connect(handler)


class DatabaseOption(object):

    def __init__(self, parent, name, example=None):
        self.name = name
        self.example = example or ''
        self.parent = parent

        self.button = QRadioButton(name, parent)
        self.button.toggled.connect(self.set_hint)

    def set_hint(self):
        self.parent.id_input.setPlaceholderText('example: ' + self.example)
        reconnect(self.parent.example_button.clicked, self.load_example)

    def load_example(self):
        self.parent.id_input.setText(self.example)


class Chooser(QDialog):

    def __init__(self, default_db='ncbi'):
        super().__init__()

        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText('Sequence ID')
        self.example_button = QPushButton('Load example')

        self.databases = {
            'ncbi': DatabaseOption(self, 'NCBI', 'NP_001009852'),
            'uniprot': DatabaseOption(self, 'Uniprot', 'P03086'),
            'ensembl': DatabaseOption(self, 'Ensembl', 'ENSP00000200691')
        }

        hbox = QHBoxLayout()
        for db_option in self.databases.values():
            button = db_option.button
            hbox.addWidget(button)
        hbox.addStretch(1)

        label_database = QLabel('Download sequence from a database: ', self)
        self.label_error = QLabel('')

        give_id = QLabel('Enter sequence ID')

        self.databases[default_db].button.toggle()
        vbox = QVBoxLayout()
        vbox.addWidget(label_database)

        vbox.addLayout(hbox)
        vbox.addWidget(give_id)
        vbox.addWidget(self.id_input)
        vbox.addWidget(self.label_error)
        vbox.addWidget(self.example_button)
        vbox.addStretch(1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

        self.setLayout(vbox)
        self.setWindowTitle('Choose database')

    def accept(self):
        sequence_id = self.id_input.text()
        if sequence_id:
            super().accept()
        self.label_error.setText("<font color='red'>No sequence ID entered.</font>")

    def get_state(self):
        sequence_id = self.id_input.text()
        database = self.get_database()

        return database, sequence_id

    def get_database(self):
        for name, db_option in self.databases.items():
            if db_option.button.isChecked():
                return name

    @staticmethod
    def choose():
        dialog = Chooser()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.get_state()
