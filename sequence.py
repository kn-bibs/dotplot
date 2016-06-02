"""Sequence reads sequence from a fasta file."""

class Sequence(object):
    """Reads sequence from a fasta file.
    
        Attributes:
            sequence: string with sequence
            name: string with sequence's name,
                read from the first line.
    """

    def __init__(self, filename):
        """Inits Sequence with empty strings as name and sequence.

        Args:
            filename - string with name of the .fasta file
        """
        self.name = ''
        self.sequence = ''
        self.read_fasta(filename)

    def read_fasta(self, filename):
        """Reads .fasta file.
        Saves sequence and its name to attributes sequence and name.

        Args:
            filename - string with name of the .fasta file
        """
        fastafile = open(filename, 'r')
        self.read_name(fastafile)
        self.read_sequence(fastafile)

    def read_sequence(self, fastafile):
        """
        Reads sequence from fasta file
        and saves it to attribute sequence as string.

        Args:
            fastafile - file in fasta format opened for reading
        """
        self.sequence = ""
        for line in fastafile:
            self.sequence += line.strip()

    def read_name(self, fastafile):
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
        self.name = name

