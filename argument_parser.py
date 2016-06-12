"""argument parser

Parses arguments
"""
import argparse
from collections import namedtuple


class ArgumentParser(object):
    """
    Parse arguments
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        sequences = self.parser.add_argument_group('sequences')
        sequences.add_argument('file1', type=argparse.FileType(),
                               help='First input file in FASTA format')
        sequences.add_argument('file2', type=argparse.FileType(),
                               help='Second input file in FASTA format')

    def parse(self, arguments):
        """
        Parse given arguments, skips first argument (assume that is script name)
        :type arguments: list
        """
        args = self.parser.parse_args(arguments[1:])
        # fixme: temporary workaround
        namedtuple1 = namedtuple(
            'Arguments', ['sequences', 'plotter', 'drawer'])
        namedtuple1.sequences = [args.file1, args.file2]
        return namedtuple1
