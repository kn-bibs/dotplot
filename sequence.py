class Sequence(object):

    def __init__(self, filename):
        self.name = ''
        self.sequence = ''
        self.read_fasta(filename)

    def read_fasta(self, filename):
        fastafile = open(filename, 'r')
        self.read_name(fastafile)
        self.read_sequence(fastafile)

    def read_sequence(self, fastafile):
        self.sequence = ""
        for line in fastafile:
            self.sequence += line.strip()

    def read_name(self, fastafile):
        name = fastafile.next()
        if not name.startswith('>'):
            raise TypeError("Not a FASTA file")
        name = name.lstrip('>')
        name = name.rstrip()
        self.name = name

