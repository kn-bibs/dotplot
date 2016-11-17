from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from dotplot import Dotplot


class MainWindow(QMainWindow):

    def __init__(self, args):
        super().__init__()

        self.sequences = args.sequences
        self.args = args

        self.init_ui()

        if self.are_sequences_loaded():
            self.new_plot()

    def are_sequences_loaded(self):
        """Sequences are correctly loaded if both file handles are not empty"""
        return self.sequences.file1 and self.sequences.file2

    def init_ui(self):
        """Initialize all GUI elements and show window."""

        self.statusBar().showMessage('Welcome')
        self.create_menus()

        canvas = self.create_canvas()
        sequence_form = self.create_sequence_form()

        # let's have the sequence form over the canvas.
        vbox = QVBoxLayout()
        vbox.addLayout(sequence_form)
        vbox.addWidget(canvas)

        interior = QWidget()
        interior.setLayout(vbox)
        self.setCentralWidget(interior)

        self.resize(500, 500)
        self.setWindowTitle('Dotplot')
        self.show()

    def new_plot(self):
        """Create and display a new plot, using current sequences and args."""

        # we require sequences to be present here!
        if not self.are_sequences_loaded():
            QMessageBox.information(
                self,
                'Sequences not selected',
                'Please, select sequences first :)'
            )
            return False

        # return to beginning of file in sequence files
        # (so we can use the same handler again if ueser wants)
        self.sequences.file1.seek(0)
        self.sequences.file2.seek(0)

        # make new dotplot
        dotplot = Dotplot(
            self.sequences,
            self.args.plotter,
            self.args.drawer
        )

        dotplot.make_plot()

        self.display_plot(dotplot)

    def select_sequence_dialog(self):
        """Invoke dialog window allowing to choose a sequence file.

        A tuple (file_name, file_type) will be returned.
        If nothing was selected the tuple will be have two empty strings.
        """
        selected_file_data = QFileDialog.getOpenFileName(
            self,
            'Open file',
            '',   # use the last (or default) directory. It HAS to be str
            'Fasta files (*.fa *.fasta);;All files (*)'
        )

        return selected_file_data

    def create_sequence_selector(self, seq_id):
        """Creates and handles widgets for a file selection."""
        from PyQt5.QtWidgets import QToolButton

        file_handle = getattr(self.sequences, 'file' + seq_id)

        current_sequence_indicator = QLabel(self)
        current_sequence_indicator.setText(
            file_handle.name if file_handle else 'Not selected'
        )

        def callback_closure():
            file_name, file_type = self.select_sequence_dialog()
            if file_name:
                file_handle = open(file_name, 'r')
                setattr(self.sequences, 'file' + seq_id, file_handle)
                current_sequence_indicator.setText(file_name)

        def callback_more():
            from chooser import Chooser
            database, sequence_name = Chooser.choose()
            if sequence_name:
                setattr(self.sequences, 'from_' + database, sequence_name)
                current_sequence_indicator.setText(sequence_name + ' (' + database + ')')

        select_btn = QPushButton('Select sequence ' + seq_id)
        select_btn.clicked.connect(callback_closure)

        more_btn = QToolButton()
        more_btn.setArrowType(Qt.DownArrow)
        more_btn.clicked.connect(callback_more)

        btn_box = QHBoxLayout()
        btn_box.setContentsMargins(0, 0, 0, 0)
        btn_box.setSpacing(0)
        btn_box.addWidget(select_btn)
        btn_box.addWidget(more_btn)

        hbox = QHBoxLayout()
        hbox.addWidget(current_sequence_indicator)
        hbox.addLayout(btn_box)

        return hbox

    def create_sequence_form(self):
        """Create whole panel for sequence selection."""
        sequence_1_selector = self.create_sequence_selector('1')
        sequence_2_selector = self.create_sequence_selector('2')
        plot_button = QPushButton('Plot!')
        plot_button.clicked.connect(self.new_plot)

        data_form = QVBoxLayout()
        data_form.addLayout(sequence_1_selector)
        data_form.addLayout(sequence_2_selector)
        data_form.addWidget(plot_button)

        return data_form

    def create_canvas(self):
        """Make widgets where the drawing will take place.

        Currently TextEdit is used - only temporarily ;)
        """
        from PyQt5.QtGui import QFont
        text_area = QLabel()
        font = QFont('Monospace', 8, QFont.TypeWriter)
        text_area.setFont(font)
        text_area.setAlignment(Qt.AlignCenter)
        self.canvas = text_area
        return text_area

    def create_menus(self):
        """Create menu entries and appropriate actions."""

        menu_bar = self.menuBar()

        action_exit = QAction(
            'E&xit', self, shortcut='Ctrl+Q',
            statusTip='Exit the application', triggered=self.close
        )

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(action_exit)

        action_about = QAction(
            '&About', self,
            statusTip='More about this app', triggered=self.about
        )

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(action_about)

    def about(self):
        """Show modal window with description of this program."""
        QMessageBox.about(
            self,
            'About Dotplot',
            'There are <i>many</i> programs that attempt to create dotplots already. Unfortunately most of these programs was created long time ago and written in old versions of Java. <p>This Python3 package will allow new generations of bioinformaticians to generate dotplots much easier.</p>')

    def display_plot(self, dotplot):
        """Display provided plot from given dotplot instance."""
        plot_text = dotplot.drawer.make_unicode(dotplot.plot)
        self.canvas.setText(plot_text)
