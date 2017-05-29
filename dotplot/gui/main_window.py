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
from PyQt5.QtWidgets import QSplitter
from ..dotplot import Dotplot
from ..sequence import DownloadFailed
from ..sequence import Sequence
from .chooser import Chooser
from .options import OptionPanel


class SequenceSelector(QHBoxLayout):

    def __init__(self, window, seq_id, current_sequence_name=None):
        """Creates and handles widgets for a file selection."""
        super().__init__()
        from PyQt5.QtWidgets import QToolButton

        self.window = window
        self.seq_id = seq_id

        if not current_sequence_name and len(self.window.sequences) >= seq_id:
            sequence = self.window.sequences[seq_id - 1]
            if sequence:
                current_sequence_name = self.window.sequences[seq_id - 1].name

        self.current_sequence_indicator = QLabel(window)
        self.current_sequence_indicator.setText(
            current_sequence_name or 'Not selected'
        )
        self.select_btn = QPushButton('Select sequence %s' % seq_id)
        self.select_btn.clicked.connect(self.callback_file)

        self.more_btn = QToolButton()
        self.more_btn.setArrowType(Qt.DownArrow)
        self.more_btn.clicked.connect(self.callback_more)

        self.btn_box = QHBoxLayout()
        self.btn_box.setContentsMargins(0, 0, 0, 0)
        self.btn_box.setSpacing(0)
        self.btn_box.addWidget(self.select_btn)
        self.btn_box.addWidget(self.more_btn)

        self.addWidget(self.current_sequence_indicator)
        self.addLayout(self.btn_box)

    def connect(self):
        self.select_btn.clicked.connect(self.callback_file)
        self.more_btn.clicked.connect(self.callback_more)

    def select_sequence_dialog(self):
        """Invoke dialog window allowing to choose a sequence file.

        A tuple (file_name, file_type) will be returned.
        If nothing was selected the tuple will be have two empty strings.
        """
        selected_file_data = QFileDialog.getOpenFileName(
            self.window,
            'Open file',
            '',  # use the last (or default) directory. It HAS to be str
            'Fasta files (*.fa *.fasta);;Plain text file (*.txt);;All files (*)',
            None,
            QFileDialog.DontUseNativeDialog
        )

        return selected_file_data

    def load_sequence(self, source_method, name, *source_specific_parameters):
        """Create and load sequence from given source, using specified parameters."""
        from os.path import basename
        constructor = getattr(Sequence, source_method)
        sequence = constructor(*source_specific_parameters)
        self.window.sequences[self.seq_id - 1] = sequence
        self.window.set_status('Sequence "%s" loaded successfully' % name)
        self.current_sequence_indicator.setText(
            '%s (%s)' % (sequence.name, basename(name))
        )
        return True

    def callback_file(self):
        file_name, file_type = self.select_sequence_dialog()

        if not file_name:
            return

        with open(file_name, 'r') as file_handle:

            if file_name.endswith('.fa') or file_name.endswith('.fasta'):
                return self.load_sequence('from_fasta_file', file_name, file_handle)
            elif file_name.endswith('.txt'):
                return self.load_sequence('from_text_file', file_name, file_handle)
            else:
                try:
                    extension = file_name.split('.')[1]
                    self.window.set_status(
                        'Unknown file extension "%s" (of file "%s")'
                        %
                        (extension, file_name)
                    )
                except IndexError:
                    self.window.set_status(
                        'No file extension detected in "%s" file name'
                        %
                        file_name
                    )
                return False

    def callback_more(self):
        result = Chooser.choose()
        if not result:  # chooser does not guarantee to return a tuple
            return
        database, sequence_name = result
        self.window.set_status('Sequence download in progress')
        try:
            self.load_sequence(
                'from_' + database,
                sequence_name + ' (' + database + ')',
                sequence_name,
                )
            self.window.set_status('Sequence downloaded successfully')
        except DownloadFailed as e:
            self.window.set_status(e.message)


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()

        self.sequences = args.parsed_sequences
        self.args = args

        self.use_matplotlib = args.drawer.method == 'matplotlib'

        self.init_ui()

        if self.are_sequences_loaded():
            self.new_plot()

    def set_status(self, text):
        self.statusBar().showMessage(text)

    def are_sequences_loaded(self):
        """Sequences are correctly loaded if both file handles are not empty"""
        return (
            len(self.sequences) >= 2 and
            self.sequences[0] and
            self.sequences[1]
        )

    def init_ui(self):
        """Initialize all GUI elements and show window."""

        self.set_status('Welcome')
        self.create_menus()

        canvas_box = self.create_canvas()
        sequence_form = self.create_sequence_form()

        # let's have the sequence form over the canvas.
        vbox = QVBoxLayout()
        vbox.addLayout(sequence_form, stretch=0)
        vbox.setAlignment(Qt.AlignTop)

        vbox.addLayout(canvas_box, stretch=1)

        splitter = QSplitter(Qt.Horizontal)

        options = OptionPanel(self.args)

        for layout in [vbox, options]:
            widget = QWidget()
            widget.setLayout(layout)
            splitter.addWidget(widget)

        self.setCentralWidget(splitter)

        self.resize(600, 600)
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

        # make new dotplot
        self.set_status('Creating a plot')
        dotplot = Dotplot(
            self.sequences,
            self.args.plotter,
            self.args.drawer
        )

        dotplot.make_plot()

        self.display_plot(dotplot)
        self.set_status('Plot created successfully')
        return True

    def select_save_file_dialog(self):
        """Supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz."""
        extensions = {'PNG file (*.png)': '.png', 'PDF file (*.pdf)': '.pdf',
                      'SVG files (*.svg, *.svgz)': '.svg', 'All files (*)': ''}
        extensions_string = ';;'.join(extensions.keys())
        file_data = QFileDialog.getSaveFileName(
            self,
            'Choose a directory',
            '',  # use the last (or default) directory. It HAS to be str
            extensions_string,
            None,
            QFileDialog.DontUseNativeDialog)
        file_name = file_data[0]
        if file_name == '':
            return
        extension = extensions[file_data[1]]
        if extension not in file_name and '.' not in file_name:
            file_name += extension
        self.canvas.save_file(file_name)

    def create_sequence_form(self):
        """Create whole panel for sequence selection."""
        sequence_1_selector = SequenceSelector(self, 1)
        sequence_2_selector = SequenceSelector(self, 2)
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
        self.canvas_box = QVBoxLayout()
        savebutton = QPushButton('Save plot to file')
        savebutton.clicked.connect(self.select_save_file_dialog)

        if self.use_matplotlib:
            from ..figures_plot import MyFigure
            self.canvas = MyFigure()
        else:
            from PyQt5.QtGui import QFont
            text_area = QLabel()
            font = QFont('Monospace', 8, QFont.TypeWriter)
            text_area.setFont(font)
            text_area.setAlignment(Qt.AlignCenter)
            text_area.setStyleSheet('font-family:Monospace,Courier')
            self.canvas = text_area

        self.canvas_box.addWidget(self.canvas)
        self.canvas_box.addWidget(savebutton)

        return self.canvas_box

    def create_menus(self):
        """Create menu entries and appropriate actions."""

        menu_bar = self.menuBar()

        action_exit = QAction(
            'E&xit', self, shortcut='Ctrl+Q',
            statusTip='Exit the application', triggered=self.close
        )

        action_save = QAction(
            'Save plot to file', self, shortcut='Ctrl+S',
            triggered=self.select_save_file_dialog
        )

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(action_exit)
        file_menu.addAction(action_save)

        action_about = QAction(
            '&About', self,
            statusTip='More about this app', triggered=self.about
        )

        action_tutorial = QAction(
            '&Tutorial', self,
            statusTip='Here should be your tutorial', triggered=self.tutorial
        )

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(action_about)
        help_menu.addAction(action_tutorial)

    def about(self):
        """Show modal window with description of this program."""
        QMessageBox.about(
            self,
            'About Dotplot',
            'There are <i>many</i> programs that attempt to create dotplots already. '
            'Unfortunately most of these programs was created long time ago and written '
            'in old versions of Java. <p>This Python3 package will allow new generations '
            'of bioinformaticians to generate dotplots much easier.</p>'
        )

    def tutorial(self):
        """Show modal window with tutorial."""
        QMessageBox.about(
            self,
            'Tutorial',
            'Microsatellites (2-5 base pairs) and minisatellies (10-50 base pairs), repeated 10-50 times are highly '
            'mutable genome regions of low complexity; they are present in telomeres. '
            'They are used in researching <s>similarity</s> between genomes.'
            '<p>Any longer section suggests a least some local similarity of studied structures. '
            'If we observe many indel regions, inversions, dotted lines while comparing sequences of two organisms, '
            'it suggests that they are related. </p>'
        )

    def display_plot(self, dotplot):
        """Display provided plot from given dotplot instance."""

        if self.use_matplotlib:
            self.canvas.reset()
            dotplot.draw(self.canvas.main_plot, self.sequences)
            self.canvas.draw()
        else:
            plot_text = dotplot.draw()
            geometry = self.frameGeometry()
            height = geometry.height() - 100
            width = geometry.width() - 100
            size = round(
                min(
                    width / len(self.sequences[0]) * 2,
                    height / len(self.sequences[1])
                ) / 2
            )
            if size == 0:
                size = 1
            self.canvas.setStyleSheet('font-size:%spx' % size)
            self.canvas.setText(plot_text)
