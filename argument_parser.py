# coding=utf-8
"""argument parser

Parses arguments
"""
import argparse


class Nestedspace(argparse.Namespace):
    """
    Helps with nesting namespaces creating foo when dest=foo.bar
    """

    def __setattr__(self, name, value):
        if '.' in name:
            group, name = name.split('.', 1)
            nested_namespace = getattr(self, group, Nestedspace())
            setattr(nested_namespace, name, value)
            self.__dict__[group] = nested_namespace
        else:
            self.__dict__[name] = value


class ArgumentParser(object):
    """
    Parse arguments
    """
    nested_namespace = Nestedspace()

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
        self.sequences.add_argument('sequences.file1',
                                    metavar='file 1',
                                    type=argparse.FileType(),
                                    help='First input file in FASTA format')
        self.sequences.add_argument('sequences.file2',
                                    metavar='file 2',
                                    type=argparse.FileType(),
                                    help='Second input file in FASTA format')

        # todo: plotter.window_size (od 1 (ew. do 1000 ale lepiej bez limitu))
        # todo: plotter.stringency (od 1 do wielkości okna do kwadratu)
        # todo: plotter.matrix (PAM250, BINARY) (użyć choice)

        # todo: drawer.true_char (jaki znak rysujemy tam, gdzie się zgadza)
        # todo: drawer.false_char(jaki znak rysujemy tam, gdzie się nie zgadza)

    def parse(self, arguments):
        """
        Parse given arguments, skips first argument (assume that is script name)
        :type arguments: list
        """
        args = self.parser.parse_args(arguments[1:], self.nested_namespace)
        args.plotter = Nestedspace()
        args.drawer = Nestedspace()
        return args
