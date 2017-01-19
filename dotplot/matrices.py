"""This module works with similarity matrices of aminoacids"""
import os


available_matrices = {
    'PAM120': 'matrices/PAM120.txt'
}


class SimilarityMatrix:

    def __init__(self, name):
        filename = available_matrices[name]

        # get the raw matrix from file
        matrix = self.read_raw_matrix(filename)

        # get minimum and maximum value from the matrix
        self.scaling_factors = self.get_min_and_max(matrix)

        # transform numerical values from raw matrix into percentages
        self.matrix = self.normalize(matrix)

    @staticmethod
    def get_min_and_max(matrix):
        """Get minimal and maximal value occuring in given matrix."""

        aminoacids = list(matrix.keys())

        minimal_value = None
        maximal_value = None

        if aminoacids:
            first_aa = aminoacids[0]

            minimal_value = matrix[first_aa][first_aa]
            maximal_value = matrix[first_aa][first_aa]

        for index_1, aa_1 in enumerate(aminoacids):
            for index_2 in range(index_1, len(aminoacids)):
                aa_2 = aminoacids[index_2]

                value = matrix[aa_1][aa_2]
                minimal_value = min(minimal_value, value)
                maximal_value = max(maximal_value, value)

        return {
            'min': minimal_value,
            'max': maximal_value
        }

    def normalize(self, matrix):
        """Transform numerical values from raw matrix into percentages.

        For example: if we had values from -5 to 5, then now:
           -5 will be 0,
            5 will be 1,
            0 will be 0.5, and so on.
        """
        aminoacids = matrix.keys()

        min_value = self.scaling_factors['min']
        max_value = self.scaling_factors['max']

        scale_range = max_value - min_value

        for aa_1 in aminoacids:
            for aa_2 in aminoacids:
                value = matrix[aa_1][aa_2]
                matrix[aa_1][aa_2] = (value - min_value) / scale_range

        return matrix

    @staticmethod
    def read_raw_matrix(filename):
        """This function converts the matrix into a dictionary"""
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            filename
        )
        with open(path) as f:
            lines = f.readlines()
            matrix = {}
            # read aminoacids' order from first line and make all the letters
            # representing aminoacids uppercase (so we don't need to think
            # about this later
            aa_list = [aa.upper() for aa in lines[0].split()]

            # initialize matrix
            for aa_name in aa_list:
                matrix[aa_name] = {}

            # set corresponding values for each aminoacid
            for line in lines[1:]:
                data = line.split()
                aa_name = data[0].upper()

                # exctract values from all the columns but the first one
                # and convert them to intigers (from strings)
                values = [
                    int(value)
                    for value in data[1:]
                ]
                matrix[aa_name] = dict(zip(aa_list, values))
        return matrix

    def get_value(self, aa_1, aa_2):
        """This function returns similarity values for 2 aminoacids

        Args:
            aa_1: a letter representing first aminoacid
            aa_2: a letter representing second aminoacid
        """
        # we want to return correct value no matter if users gives us
        # aa_1 = t, aa_2 = c or aa_1 = T, aa_2 = C, hence uppercase
        aa_1 = aa_1.upper()
        aa_2 = aa_2.upper()
        return self.matrix[aa_1][aa_2]
