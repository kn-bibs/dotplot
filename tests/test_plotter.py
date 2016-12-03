from plotter import Plotter
from sequence import Sequence

def test_window_matrix():

    p = Plotter()
    s1 = Sequence('ABCABC', 'Test Sequence 1')
    s2 = Sequence('ABAABA', 'Test Sequence 2')
    assert p.windows_matrix([s1, s2]) == [[1, 1, 1, 1], [0, 0, 0], [0, 0, 0]]

def test_append_to_scores():

    p = Plotter()
    scores = [[]]
    p.append_to_scores(5, scores)
    p.append_to_scores(1, scores)
    p.append_to_scores(0, scores)
    assert scores == [[1, 0, 0]]
