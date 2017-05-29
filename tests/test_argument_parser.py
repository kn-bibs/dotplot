import pytest
import argparse
from dotplot.argument_parser import positive_int
from dotplot.argument_parser import NestedNamespace


def test_nested_namespace():
    namespace = NestedNamespace()

    namespace.x = 5
    assert namespace.x == 5

    assert namespace.get('y', 15) == 15

    with pytest.raises(AttributeError):
        namespace.y

    namespace.y = 10
    assert namespace.y == 10


def test_positive_int():

    with pytest.raises(argparse.ArgumentTypeError):
        positive_int('-5')

    with pytest.raises(argparse.ArgumentTypeError):
        positive_int('0')

    assert positive_int('1') == 1

    assert positive_int('+10') == 10
