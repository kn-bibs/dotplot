from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit


class Choose(QWidget):
    def __init__(self):
        super().__init__()

        self.ncbi = QRadioButton('NCBI ', self)
        self.uniprot = QRadioButton('Uniprot', self)
        self.ensembl = QRadioButton('Ensembl', self)

        label_database = QLabel('Download sequence from a database: ', self)
        self.label_error = QLabel('')

        hbox = QHBoxLayout()
        hbox.addWidget(self.ncbi)
        hbox.addWidget(self.uniprot)
        hbox.addWidget(self.ensembl)
        hbox.addStretch(1)

        give_id = QLabel('Enter sequence ID')
        self.id_input = QLineEdit(self)
        download = QPushButton('Download', self)
        download.clicked.connect(self.download)

        vbox = QVBoxLayout()
        vbox.addWidget(label_database)

        vbox.addLayout(hbox)
        vbox.addWidget(give_id)
        vbox.addWidget(self.id_input)
        vbox.addWidget(download)
        vbox.addWidget(self.label_error)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle('Choose database')
        self.show()

    def download(self):

        sequence_id = self.id_input.text()

        if not sequence_id:
            self.label_error.setText('Enter sequence ID')

        if self.ncbi.isChecked():
            database = 'ncbi'
        elif self.uniprot.isChecked():
            database = 'uniprot'
        elif self.ensembl.isChecked():
            database = 'ensembl'
        else:
            self.label_error.setText('No database is selected')

        try:
            return sequence_id, database
        except UnboundLocalError:
            return None
