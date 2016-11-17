"""Sequence reads sequence from a fasta file or downloads it from Ensembl."""

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
            if line[0].isalpha():
                sequence += line.strip()
            else:
                print("More than one sequence found in the file: " + str(fastafile.name))
                break
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
        sequence, name = cls.get_sequence(address)
        return cls(sequence, name)

    @classmethod
    def from_uniprot(cls, uniprot_id):
        """
        Takes ID from Uniprot database, returns name and
        sequence as strings.
        """

        server = "http://www.uniprot.org/uniprot/"
        address = server + uniprot_id + ".fasta"
        sequence, name = cls.get_sequence(address)
        return cls(sequence, name)

    @classmethod
    def from_ncbi(cls, ncbi_id):
        """
        Takes ID from NCBI database, returns name and
        sequence as strings using Entrez Programming Utilities (E-utilities)
        """

        base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
        end = '/efetch.fcgi?'
        address = base + end + 'db=protein&id=' + ncbi_id + '&rettype=fasta'
        sequence, name = cls.get_sequence(address)
        return cls(sequence, name)

    @staticmethod
    def get_sequence(address):
        """
        Tries 3 times to download a sequence from given address, raises exception
        if download fails. Returns sequence and its name as strings.
        """
        ask = False
        i = 0
        while i < 3 and not ask:
            ask = requests.get(address, headers={"Content-Type": "text/x-fasta"})
            i += 1
            if not ask:
                print("Download failed. Trying again.")
        if not ask:
            raise Exception("After 3 attempts sequence downloading failed.")
        else:
            print("Sequence downloaded successfully.")

            result = ask.text.split('\n')
            name = result[0].strip('>')
            sequence = ''.join(result[1:])
            try:
                sequence[0].isalpha()
                return sequence, name
            except IndexError:
                raise Exception("Sequence not found")
