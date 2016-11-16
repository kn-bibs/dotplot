"""argument parser
Parses arguments
"""
import argparse


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


class ArgumentParser(object):
    """
    Parse arguments
    """
    nested_namespace = NestedNamespace()

    def __init__(self):
        """
        If you want add:
            positional argument
                you should specify it name as you want to access it
                and use metavar parameter to set display name
            optional argument
                you should specify dest as you want to access it
        In all cases we should use group arguments to display help properly

        """
        self.parser = argparse.ArgumentParser()

        self.sequences = self.parser.add_argument_group('sequences')
        self.sequences.add_argument(
            'sequences.file1',
            metavar='file 1',
            nargs='?',
            type=argparse.FileType(),
            help='First input file in FASTA format'
        )
        self.sequences.add_argument(
            'sequences.file2',
            metavar='file 2',
            nargs='?',
            type=argparse.FileType(),
            help='Second input file in FASTA format'
        )

        self.parser.add_argument(
            '--gui',
            dest='gui',
            action='store_true',
            help=(
                'Run the program in Graphical Interface mode.' +
                ' If specified no additional arguments are required.'
            )
        )
        # todo: plotter.window_size (from 1 (possibly to 1000, but better without upper limitation))
        # todo: plotter.stringency (from 1 to squared window_size)
        # todo: plotter.matrix (PAM250, BINARY) (use choice)

        # todo: drawer.true_char (what char when match)
        # todo: drawer.false_char(what char when mismatch)

    def parse(self, arguments):
        """
        Parse given arguments, skips first argument (assume that is script name)
        :type arguments: list
        """
        args = self.parser.parse_args(arguments[1:], self.nested_namespace)
        args.plotter = NestedNamespace()
        args.drawer = NestedNamespace()

        args = self.interpret_arguments(args)

        return args

    def interpret_arguments(self, args):
        """Let's try to be more intelligent and guess what the user wants."""
        # if we don't have both files given, then:
        if not (args.sequences.file1 and args.sequences.file2):
            # force mode to be GUI
            if not args.gui:
                print('Not enough input files given - switching to GUI mode')
                args.gui = True
        return args
