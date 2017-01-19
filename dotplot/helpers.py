def is_pyqt5_available():
    """Check if the PyQt module is installed and importable."""
    try:
        import PyQt5 as _   # 'as _' tells pylint to ignore this variable
        return True
    except ImportError:
        return False


def is_matplotlib_available():
    """Check if the matplotlib module is installed and importable."""
    try:
        import matplotlib as _
        return True
    except ImportError:
        return False
