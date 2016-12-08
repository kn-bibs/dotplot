from plotter import Plotter
from sequence import Sequence


def test_window_matrix():

    p = Plotter()
    p.window_size = 3
    p.stringency = 2

    # test case zero:
    s1 = Sequence('', 'Test Sequence 1')
    s2 = Sequence('', 'Test Sequence 2')

    assert p.windows_matrix([s1, s2]) == [[]]

    # typical usage:
    p.window_size = 2
    s1 = Sequence('ABCDBB', 'Test Sequence 1')
    s2 = Sequence('ABAABC', 'Test Sequence 2')
    assert p.windows_matrix([s1, s2]) == [
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1]
    ]

    # typical usage:
    p.window_size = 3
    p.stringency = None
    s1 = Sequence('ABCDBB', 'Test Sequence 1')
    s2 = Sequence('ABAABC', 'Test Sequence 2')
    assert p.windows_matrix([s1, s2]) == [
        [3/9, 3/9, 3/9, 3/9],
        [1/9, 1/9, 1/9, 2/9],
        [1/9, 1/9, 1/9, 2/9],
        [2/9, 2/9, 2/9, 2/9]
    ]

    # unequal length:
    p.window_size = 2
    p.stringency = 2
    s1 = Sequence('ABAABA', 'Test Sequence 1')
    s2 = Sequence('ABB', 'Test Sequence 2')
    assert p.windows_matrix([s1, s2]) == [
        [1, 1],
        [1, 1],
        [1, 0],
        [1, 1],
        [1, 1]
    ]


def test_append_to_scores():

    p = Plotter()
    scores = [[]]
    p.append_to_scores(5, scores)
    p.append_to_scores(1, scores)
    p.append_to_scores(0, scores)
    assert scores == [[5, 1, 0]]


def test_normalize_scores_to_percentage():

    p = Plotter()
    p.window_size = 2

    scores = [
        [1, 3, 0],
        [4, 2, 1],
        [3, 1, 1]
    ]
    p.normalize_scores_to_percentage(scores)

    assert scores == [
        [1/4, 3/4, 0/4],
        [4/4, 2/4, 1/4],
        [3/4, 1/4, 1/4]
    ]


def test_apply_stringency():

    p = Plotter()
    p.stringency = 3

    scores = [
        [1, 3, 0],
        [4, 2, 1],
        [3, 1, 1]
    ]
    p.apply_stringency(scores)

    assert scores == [
        [0, 1, 0],
        [1, 0, 0],
        [1, 0, 0]
    ]
