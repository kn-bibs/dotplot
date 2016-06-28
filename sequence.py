"""Sequence reads sequence from a fasta file or downloads it from Ensembl."""

import sys
import requests


class Sequence(object):
    """Reads sequence from a fasta file.
        Attributes:
            sequence: string with sequence
            name: string with sequence's name,
                read from the first line.
    """

    def __init__(self, sequence, name):
        """Inits Sequence with empty strings as name and sequence.

        Args:
            sequence - sequence (string)
            name - sequences' name (string)
        """
        self.name = name
        self.sequence = sequence

    @classmethod
    def from_fasta_file(cls, fastafile):
        """Reads .fasta file.
        Saves sequence and its name to attributes sequence and name.

        Args:
            fastafile - fasta file open for reading.
        """
        name = cls.read_name(fastafile)
        sequence = cls.read_sequence(fastafile)
        return cls(sequence, name)

    @staticmethod
    def read_sequence(fastafile):
        """
        Reads sequence from fasta file
        and saves it to attribute sequence as string.

        Args:
            fastafile - file in fasta format opened for reading
        """
        sequence = ''
        for line in fastafile:
            sequence += line.strip()
        return sequence

    @staticmethod
    def read_name(fastafile):
        """
        Reads sequence's name from fasta file
        and saves it to attribute name as string.
        Checks if first line starts with '>',
        raises TypeError if not.

        Args:
            fastafile - file in fasta format opened for reading
        """
        name = fastafile.readline()
        if not name.startswith('>'):
            raise TypeError("Not a FASTA file")
        name = name.lstrip('>')
        name = name.rstrip()
        return name

    @classmethod
    def from_ensembl(cls, ensembl_id):
        """
        Takes ID from Ensembl database, returns name and
        sequence as strings.
        """

        server = "http://rest.ensembl.org"
        ext = "/sequence/id/" + ensembl_id + "?"
        address = server + ext

        ask = requests.get(address, headers={"Content-Type": "text/x-fasta"})

        if not ask.ok:
            ask.raise_for_status()
            sys.exit()

        result = ask.text.split('\n')
        name = result[0].strip('>')
        sequence = ''.join(result[1:])
        return cls(sequence, name)
