"""Sequence reads sequence from a fasta file."""

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
    def from_fasta_file(cls, filename):
        """Reads .fasta file.
        Saves sequence and its name to attributes sequence and name.

        Args:
            filename - string with name of the .fasta file
        """
        fastafile = open(filename, 'r')
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
        name = fastafile.next()
        if not name.startswith('>'):
            raise TypeError("Not a FASTA file")
        name = name.lstrip('>')
        name = name.rstrip()
        return name

