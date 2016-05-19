class Plotter(object):

    def __init__(self, *args, **kwargs):
        self.dotmatrix = []

    def plot(self, sequences):
        """
        Creates dotplot matrix for given sequences

        Parameters: (str, str) - sequences to analyse
        Return: list of lists of ints - dotplot matrix for sequences
        """
        seq1, seq2 = sequences

        for row_index, vertical_letter in enumerate(seq1):
            self.dotmatrix.append([])
            for horizontal_letter in seq2:
                if horizontal_letter == vertical_letter:
                    self.dotmatrix[row_index].append(1)
                else:
                    self.dotmatrix[row_index].append(0)
        return self.dotmatrix

