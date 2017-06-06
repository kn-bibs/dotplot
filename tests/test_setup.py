from setup import get_long_description


def test_get_long_description():
    description = get_long_description('README.md')
    assert description and type(description) is str
