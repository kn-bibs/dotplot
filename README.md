# Dotplot
[![Code Climate](https://codeclimate.com/github/kn-bibs/dotplot/badges/gpa.svg)](https://codeclimate.com/github/kn-bibs/dotplot) [![Test Coverage](https://codeclimate.com/github/kn-bibs/dotplot/badges/coverage.svg)](https://codeclimate.com/github/kn-bibs/dotplot/coverage)


## Idea

Dotplot is a plot used mainly in biology for graphical visualisations of sequences' similarity. [Read more on Wikipedia] (https://en.wikipedia.org/wiki/Dot_plot_%28bioinformatics%29).

## Why to create a new package?

There are many programs that attempt to create dotplots already. Unfortunately most of these programs was created long time ago and written in old versions of Java. This Python3 package will allow new generations of bioinformaticians to generate dotplots much easier.

## Installation & usage
```bash
git clone https://github.com/kn-bibs/dotplot
```

To use graphical user interface, you will need to have pyqt5 installed, e.g. with:
```python3
sudo pip3 install pyqt5
```

### Basic usage

```bash
cd dotplot
```

```bash
python3 dotplot.py seq1.fasta seq2.fasta
```
To use graphical user interface, type: 

```bash
python3 dotplot.py seq1.fasta seq2.fasta --gui
```

#### Getting help

To access list of available options run command above with added option `-h`.

## What will it do?
In the future our application will be able to read a wide range of input formats, and users will be able to parametrize alignment process and output format to their liking. 

## Dependencies & development
We are writing in `Python3` and strict on code styling, with pep8 and pylint validation. We require all code merging to master to have at least 7,5 pylint score. To check this, at first install pytlint with pip3 and then, run the following command: `python3 -m pylint dotplot.py`, where in place of `dotplot.py` use any name of the module to be tested. 
