import pytest
import argparse
from dotplot.argument_parser import positive_int


def test_positive_int():

    with pytest.raises(argparse.ArgumentTypeError):
        positive_int('-5')

    with pytest.raises(argparse.ArgumentTypeError):
        positive_int('0')

    assert positive_int('1') == 1

    assert positive_int('+10') == 10
