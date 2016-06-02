"""argument parser

Parses arguments
"""
import argparse


class ArgumentParser(object):
    """
    Parse arguments
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file1', type=argparse.FileType(),
                                 help='First input file in FASTA format')
        self.parser.add_argument('file2', type=argparse.FileType(),
                                 help='Second input file in FASTA format')

    def parse(self, arguments):
        """
        Parse given arguments, skips first argument (assume that is script name)
        :type arguments: list
        """
        return vars(self.parser.parse_args(arguments[1:]))
