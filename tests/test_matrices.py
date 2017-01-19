from dotplot.matrices import SimilarityMatrix
from argparse import Namespace


def test_get_min_and_max():

    # scenario 1: different min and max
    matrix = {
        'A': {'A': 15, 'B': -5},
        'B': {'A': -5, 'B': 10}
    }

    assert SimilarityMatrix.get_min_and_max(matrix) == {
        'min': -5,
        'max': 15
    }

    # scenario 2: the same min and max
    matrix = {
        'A': {'A': 5, 'B': 5},
        'B': {'A': 5, 'B': 5}
    }

    assert SimilarityMatrix.get_min_and_max(matrix) == {
        'min': 5,
        'max': 5
    }


def test_normalize():

    dummy_instance = Namespace(
        scaling_factors={
            'min': -100,
            'max': +100
        }
    )

    matrix = {
        'A': {'A': -100, 'B': 0},
        'B': {'A': 0, 'B': 50}
    }

    assert SimilarityMatrix.normalize(dummy_instance, matrix) == {
        'A': {'A': 0, 'B': 0.5},
        'B': {'A': 0.5, 'B': 0.75}
    }


def test_read_raw_matrix():

    raw_matrix = SimilarityMatrix.read_raw_matrix(
        'matrices/PAM120.txt'
    )

    assert raw_matrix

    # are generated values numerical?
    from numbers import Number

    aminoacids = list(raw_matrix.keys())
    some_aa = aminoacids[0]

    some_value = raw_matrix[some_aa][some_aa]

    assert isinstance(some_value, Number)

    # possible future tests:
    # - is generated matrix symetrical?
    # - is generated matrix of n times n size?


def test_get_value():

    matrix = SimilarityMatrix('PAM120')

    # commutative property
    assert matrix.get_value('a', 'c') == matrix.get_value('c', 'a')

    # letter case shouldn't matter
    assert matrix.get_value('a', 'c') == matrix.get_value('A', 'C')

