"""Plotter creates the matrix that is later displayed."""


class Plotter(object):
    """Creates dotmatrix.

        Attributes:
            dotmatrix (list of lists of ints): representing
                dotplot matrix for two analysed sequences.
    """

    def __init__(self, *args, **kwargs):
        """Inits Plotter with empty dotmatrix."""
        self.dotmatrix = []

        # temporary values
        self.window_size = 3
        self.stringency = 2
        self.scores = {}

    def make_plot(self, sequences):
        """Creates dotplot matrix for given sequences.

        Args:
            sequences - (Sequence, Sequence): tuple of strings
                representing sequences to analyse.

        Returns:
            A list of lists of ints (matrix-like)
                representing dotplot matrix for the sequences:
                1 in places where corresponding letters agree,
                0 in places where corresponding letters do not agree.

            For example:
               sequences = ("ABA", "ABC")

                   A   B   C
                A  1   0   0
                B  0   1   0
                A  1   0   0

                [[1, 0, 0], [0, 1, 0], [1, 0, 0]] is returned

        """
        seq1 = sequences[0].sequence
        seq2 = sequences[1].sequence

        for row_index, vertical_letter in enumerate(seq1):
            self.dotmatrix.append([])
            for horizontal_letter in seq2:
                if horizontal_letter == vertical_letter:
                    self.dotmatrix[row_index].append(1)
                else:
                    self.dotmatrix[row_index].append(0)

    def plot(self, sequences):
        self.make_plot(sequences)
        return self.dotmatrix

    def get_score(self, first, second):
        # Template for function that returns score of two compared symbols
        # TODO create scoring matrix
        if first == second:
            return 1
        return 0

    def windows_matrix(self, sequences):
        # chyba dziala, ale i tak trzeba to poprawic
        seq1 = sequences[0].sequence
        seq2 = sequences[1].sequence

        scores = [[]]
        current_score = 0

        for i in range(self.window_size):
            for j in range(self.window_size):
                current_score += self.get_score(seq1[i], seq2[j])
        self.append_to_scores(current_score, scores)

        for row in range(len(seq1) - self.window_size):
            for col in range(len(seq2) - self.window_size):
                for i in range(self.window_size):
                    current_score -= self.get_score(seq1[row+i], seq2[col])
                    current_score += self.get_score(seq1[row+i],
                                                    seq2[col + self.window_size])
                self.append_to_scores(current_score, scores)
            current_score = scores[-1][0]
            for i in range(self.window_size):
                current_score -= self.get_score(seq1[row], seq2[i])
                current_score += self.get_score(seq1[row + self.window_size],
                                                seq2[i])
            scores.append([])
        return scores[:-1]

    def append_to_scores(self, current_score, scores):
        if current_score > self.stringency:
            scores[-1].append(1)
        else:
            scores[-1].append(0)
        
