"""Plotter creates the matrix that is later displayed."""
from .matrices import SimilarityMatrix


class Plotter(object):
    """Creates dotmatrix.

        Attributes:
            dotmatrix (list of lists of ints): representing
                dotplot matrix for two analysed sequences.
    """

    def __init__(self, arguments):
        """Inits Plotter with empty dotmatrix."""
        self.dotmatrix = []

        self.window_size = arguments.window_size
        self.stringency = arguments.stringency

        self.similarity_matrix = None

        matrix_name = arguments.matrix
        if matrix_name:
            self.similarity_matrix = SimilarityMatrix(matrix_name)

    def make_plot(self, sequences):
        """Creates dotplot matrix for given sequences.

        Args:
            sequences: (Sequence, Sequence):
                tuple of Sequene objects with sequences to analyse

        Returns:
            A list of lists of numbers (representing a matrix)
        """

        if self.window_size == 1:
            matrix = self.make_simple_plot(sequences)
        else:
            matrix = self.make_windowed_plot(sequences)

        self.dotmatrix = matrix

        return matrix

    def make_simple_plot(self, sequences):
        """Creates dotplot matrix for given sequences. It is a special,
        optimized case of `make_windowed_plot`: for `window_size` equal to one.

        Args:
            sequences: (Sequence, Sequence):
                tuple of Sequene objects with sequences to analyse

        Returns:
            A list of lists of floats or ints (representing a matrix).

            The exact elements in the matrix will vary accordingly to chosen
            `get_score` function. If the current scoring function has binary
            values, then the result will have:
                1 in places where corresponding symbols in sequence agree,
                0 in places where corresponding symbols do not agree.

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

        dotmatrix = []

        for vertical_letter in seq1:
            dotmatrix.append([])
            for horizontal_letter in seq2:
                score = self.get_score(vertical_letter, horizontal_letter)
                dotmatrix[-1].append(score)

        return dotmatrix

    def plot(self, sequences):
        self.make_plot(sequences)
        return self.dotmatrix

    def get_score(self, first, second):
        if self.similarity_matrix:
            return self.similarity_matrix.get_value(first, second)
        else:
            if first == second:
                return 1
            return 0

    def make_windowed_plot(self, sequences, jump=1):
        """Generate matrix of scores using window sliding techinque.

        Partial scores for particular sequence elements will be calculated
        using `get_score` method.

        Sum of partial scores from all cells belonging to given window will
        then decide about the value/score of this window:
            if `self.stringency` is set it will be one if score is higher than
            specified stringency otherwise zero; if stringency is not given the
            score divided by count of window cells (percentage) will be used.

        `self.window_size` defines size of the window.

        Args:
            sequences: (Sequence, Sequence):
                tuple of Sequene objects with sequences to analyse

            jump: how wide should each jump of the window be? If you want:
                - to slide smoothly step-by-step, leave it equal to one
                - windows not to overlap completely, use jump = window_size

        Returns:
            A list of lists of floats or ints (representing a matrix)

            Note that for N x M input (sequences) you will get
            (N - w) // j x (M - w) // j output (where j is jump, w window_size)
        """
        seq1 = sequences[0].sequence
        seq2 = sequences[1].sequence

        if not seq1 or not seq2:
            return [[]]

        window_size = self.window_size

        shortest_seq_len = min(len(seq1), len(seq2))
        if shortest_seq_len < window_size:
            window_size = shortest_seq_len

        # a matrix of scores indexed by [row][column] convention
        scores = [[]]

        # score in a current window
        current_score = 0

        # calculate score for the first, left-top window.
        # for window_size = 2 it would refer to following cells:
        # |XX     |
        # |XX     |
        # |       |
        for i in range(window_size):
            for j in range(window_size):
                current_score += self.get_score(seq1[i], seq2[j])

        self.append_to_scores(current_score, scores)

        sliding_steps_down = (len(seq1) - window_size) // jump
        sliding_steps_right = (len(seq2) - window_size) // jump

        def slide_right(row):
            """Slide window over a row in the sequence matrix to right and
            save obtained scores.

            Function moves window x positions right (where x is a jump size),
            recalculates `current_score` (removing partial scores from cells
            which are no longer in windows view, adding partial scores from
            cells just discovered) and appends it to the last row of window's
            scores matrix.

            As the function does not starts but only elongates the list of
            windows' scores (like RNA polymerase II), it requires the
            last row of scores matrix to have length equal to one.
            """
            nonlocal current_score

            assert len(scores[-1]) == 1

            for col in range(sliding_steps_right):

                # for each cell in height of the window
                for h in range(window_size):

                    # remove partial scores from those cells which we are no
                    # longer interested in (which will be left on the left
                    # to the window)
                    # and add partial scores of those cells which are to the
                    # right of our window, by extend of the specified jump.
                    for w in range(jump):
                        current_score -= self.get_score(
                            seq1[row + h], seq2[col + w]
                        )
                        current_score += self.get_score(
                            seq1[row + h], seq2[col + w + window_size]
                        )

                # we moved the window one jump right; let's remember score here
                self.append_to_scores(current_score, scores)

        # we need to have this initialized (for later use)
        row = -1

        # slide window, jump by jump to the right (by columns)
        # and then jump down and repeat
        for row in range(sliding_steps_down):
            slide_right(row)

            # get a score of the leftmost window from the recently laid layer
            # |XXXXXXXXXX|      X - we already visited those cells
            # |**XXXXXXXX|      * - also visited, the score of window covering
            # |**XXXXXXXX|          those cells will be used as current
            # |          |
            current_score = scores[-1][0]

            # move the window down by one jump, so for jump = 1 we end up with:
            # |XXXXXXXXXX|
            # |XXXXXXXXXX|
            # |**XXXXXXXX|
            # |**        |
            for w in range(window_size):
                for h in range(jump):
                    current_score -= self.get_score(
                        seq1[row + h], seq2[w]
                    )
                    current_score += self.get_score(
                        seq1[row + h + window_size], seq2[w]
                    )

            # begin next layer (row) of windows' scores (seq row != window row)
            scores.append([])
            self.append_to_scores(current_score, scores)

        # fill in the last scores' row, sliding the window over
        # corresponding sequence cells
        slide_right(row + 1)

        if self.stringency is None:
            self.normalize_scores_to_percentage(scores)
        else:
            self.apply_stringency(scores)

        return scores

    @staticmethod
    def append_to_scores(current_score, scores):
        """Append new score to the last (current) row in scores matrix."""
        scores[-1].append(current_score)

    def apply_stringency(self, scores):
        """Modify input matrix: place ones if value >= stringenccy, else 0."""
        for row in scores:
            for i, value in enumerate(row):
                row[i] = 1 if value >= self.stringency else 0

    def normalize_scores_to_percentage(self, scores):
        """Modify input matrix: divide each value by field of the window."""
        window_field = pow(self.window_size, 2)
        for row in scores:
            for i, value in enumerate(row):
                row[i] = value / window_field
