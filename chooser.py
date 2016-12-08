from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QLineEdit


class Chooser(QDialog):
    def __init__(self):
        super().__init__()

        self.ncbi = QRadioButton('NCBI ', self)
        self.uniprot = QRadioButton('Uniprot', self)
        self.ensembl = QRadioButton('Ensembl', self)
        self.ncbi.toggled.connect(self.set_hint)
        self.uniprot.toggled.connect(self.set_hint)
        self.ensembl.toggled.connect(self.set_hint)

        label_database = QLabel('Download sequence from a database: ', self)
        self.label_error = QLabel('')

        hbox = QHBoxLayout()
        hbox.addWidget(self.ncbi)
        hbox.addWidget(self.uniprot)
        hbox.addWidget(self.ensembl)
        hbox.addStretch(1)

        give_id = QLabel('Enter sequence ID')
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText('Sequence ID')

        self.ncbi.toggle()
        vbox = QVBoxLayout()
        vbox.addWidget(label_database)

        vbox.addLayout(hbox)
        vbox.addWidget(give_id)
        vbox.addWidget(self.id_input)
        #vbox.addWidget(download)
        vbox.addWidget(self.label_error)
        vbox.addStretch(1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

        self.setLayout(vbox)
        self.setWindowTitle('Choose database')
        #self.show()

    def accept(self):
        sequence_id = self.id_input.text()
        if sequence_id:
            super().accept()
        self.label_error.setText("<font color='red'>No sequence ID entered.</font>")

    def get_state(self):
        sequence_id = self.id_input.text()
        database = self.get_database()

        return database, sequence_id
    """
        try:
            return database, sequence_id
        except UnboundLocalError:
            return False"""

    def get_database(self):
        if self.ncbi.isChecked():
            return 'ncbi'
        elif self.uniprot.isChecked():
            return 'uniprot'
        elif self.ensembl.isChecked():
            return 'ensembl'

    def set_hint(self):
        placeholders = {
            'ncbi': 'example: NC_000017.11',
            'uniprot': 'example: P97929',
            'ensembl': 'example: ENSG00000157764'
        }
        database = self.get_database()

        hint = placeholders[database]

        self.id_input.setPlaceholderText(hint)

    @staticmethod
    def choose():
        dialog = Chooser()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.get_state()
