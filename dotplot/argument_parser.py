"""
Parses arguments and performs basic validation.
"""
import argparse
from collections import defaultdict
from .sequence import Sequence
from .drawer import Drawer


class NestedNamespace(argparse.Namespace):
    """
    Helps with nesting namespaces creating foo when dest=foo.bar
    """

    def __setattr__(self, name, value):
        if '.' in name:
            group, name = name.split('.', 1)
            nested_namespace = getattr(self, group, NestedNamespace())
            setattr(nested_namespace, name, value)
            self.__dict__[group] = nested_namespace
        else:
            self.__dict__[name] = value

    def get(self, name, default):
        if '.' in name:
            # TODO
            raise NotImplementedError
        try:
            return getattr(self, name)
        except AttributeError:
            return default


def positive_int(string):
    """Validate given string as a positive integer and return it casted to int.

    Raises:
        argparse.ArgumentTypeError: when string represents negative int or 0.
    """
    value = int(string)

    if value < 1:
        raise argparse.ArgumentTypeError(
            '%s is not a positive integer' % string
        )

    return value


class ArgumentParser(object):
    """Parse and interpret arguments."""
    nested_namespace = NestedNamespace()

    sequence_sources = [
        'from_text_file',
        'from_fasta_file',
        'from_ensembl',
        'from_uniprot',
        'from_ncbi'
    ]

    def __init__(self):
        """
        If you want to add:
            positional argument
                you should specify its name as you want to access it
                and use metavar parameter to set display name
            optional argument
                you should specify dest as you want to access it
        In all cases we should use group arguments to display help properly

        """
        self.parser = argparse.ArgumentParser()

        self.sequences = self.parser.add_argument_group('input sequences')
        self.drawer = self.parser.add_argument_group('display options')
        self.plotter = self.parser.add_argument_group('plot generation')

        # general
        self.parser.add_argument(
            '--gui',
            dest='gui',
            action='store_true',
            help=(
                'Run the program in Graphical Interface mode.'
                ' If specified no additional arguments are required.'
            )
        )

        # drawer
        self.drawer.add_argument(
            '--drawer',
            dest='drawer.method',
            choices=Drawer({}).drawing_methods.keys(),
            help=(
                'Choose a drawing method. Defaults to matplotlib in GUI mode'
                ' and to unicode for console mode.'
            )
        )

        self.drawer.add_argument(
            '--show_sequences',
            dest='drawer.show_sequences',
            default=100,
            help=(
                'Choose if matplotlib should show sequences on axes. '
                'True/False or the maximum lenght of a sequence which will be shown.'
            )
        )
        # plotter
        self.plotter.add_argument(
            '--window_size',
            dest='plotter.window_size',
            type=positive_int,
            default=1,
            help=(
                'Choose window size. Defaults to one.'
            )
        )
        self.plotter.add_argument(
            '--matrix',
            dest='plotter.matrix',
            choices=['PAM120', None],
            default=None,
            help=(
                'Choose matrix. By default no matrix is used.'
            )
        )

        # stringency
        self.plotter.add_argument(
            '--stringency',
            dest='plotter.stringency',
            type=positive_int,
            default=None,
            help=(
                'Choose stringency. Defaults to none.'
            )
        )

        # sequences - local
        self.sequences.add_argument(
            '--fasta',
            dest='sequences.from_fasta_file',
            metavar='filename',
            nargs='*',
            type=argparse.FileType(),
            help='Input file(s) in FASTA format'
        )

        self.sequences.add_argument(
            '--txt',
            dest='sequences.from_text_file',
            metavar='filename',
            nargs='*',
            type=argparse.FileType(),
            help='Input plain file(s) like *.txt'
        )
        # sequences - remote
        self.sequences.add_argument(
            '--ncbi',
            dest='sequences.from_ncbi',
            metavar='ncbi_id',
            nargs='*',
            type=str,
            help=(
                'Run the program downloading sequences from NCBI database. '
                'For example: --ncbi NC_000017.11 NC_000071.6'
            )
        )
        self.sequences.add_argument(
            '--uniprot',
            dest='sequences.from_uniprot',
            metavar='uniprot_id',
            nargs='*',
            type=str,
            help=(
                'Run the program downloading sequences from Uniprot database. '
                'For example: --uniprot P48754 P97929'
            )
        )
        self.sequences.add_argument(
            '--ensembl',
            dest='sequences.from_ensembl',
            metavar='ensembl_id',
            nargs='*',
            type=str,
            help=(
                'Run the program downloading sequences from Ensembl database. '
                'For example: --ensembl ENSG00000157764 ENSG00000157764'
            )
        )

        # todo: drawer.true_char (what char when match)
        # todo: drawer.false_char(what char when mismatch)

    def parse(self, arguments):
        """Parse command-line arguments into nested namespaces.

        The first arg will be skipped: we assume that it's the script name.
        """
        args = self.parser.parse_args(arguments[1:], self.nested_namespace)
        args = self.interpret_arguments(args)

        return args

    def parse_sequences(self, sequence_arguments):
        """Extract sequence data from arguments and load sequences."""
        parsed_sequences = defaultdict()
        seq_nr = 0
        for source in self.sequence_sources:
            sequence_list = getattr(sequence_arguments, source) or []
            for value in sequence_list:
                constructor = getattr(Sequence, source)
                parsed_sequences[seq_nr] = constructor(value)
                seq_nr += 1
        return parsed_sequences

    def interpret_arguments(self, args):
        """Let's try to be more intelligent and guess what the user wants."""
        # if we don't have both files given, then:
        args.parsed_sequences = self.parse_sequences(args.sequences)

        if (
            args.plotter.stringency and
            args.plotter.stringency > pow(args.plotter.window_size, 2)
        ):
            print(
                'Warning: stringency is greater than size of window squared'
                ' what does not make sense'
            )

        if len(args.parsed_sequences) > 2:
            print('Too many sequences given')

        if len(args.parsed_sequences) < 2:
            # force mode to be GUI
            if not args.gui:
                print('Not enough sequences given - switching to GUI mode')
                args.gui = True

        # set drawer method to defaults if not set
        if not args.drawer.method:
            from .helpers import is_matplotlib_available

            method = 'unicode'

            if args.gui:
                if is_matplotlib_available():
                    method = 'matplotlib'

            args.drawer.method = method

        return args
