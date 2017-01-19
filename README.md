# Dotplot
[![Build Status](https://travis-ci.org/kn-bibs/dotplot.svg?branch=master)](https://travis-ci.org/kn-bibs/dotplot) [![Code Climate](https://codeclimate.com/github/kn-bibs/dotplot/badges/gpa.svg)](https://codeclimate.com/github/kn-bibs/dotplot) [![Coverage Status](https://coveralls.io/repos/github/kn-bibs/dotplot/badge.svg)](https://coveralls.io/github/kn-bibs/dotplot) 


## Idea

Dotplot is a plot used mainly in biology for graphical visualisations of sequences' similarity. [Read more on Wikipedia] (https://en.wikipedia.org/wiki/Dot_plot_%28bioinformatics%29).

## Why to create a new package?

There are many programs that attempt to create dotplots already. Unfortunately most of these programs was created long time ago and written in old versions of Java. This Python3 package will allow new generations of bioinformaticians to generate dotplots much easier.

## Installation & usage

### Instalation with pip

The easiest way to install this package with all dependencis is to use pip:

```bash
pip install dotplot
```

### Manual installation

```bash
git clone https://github.com/kn-bibs/dotplot
```

To use graphical user interface, you will need to have pyqt5 installed, e.g. with:
```python3
sudo apt-get install python3-pyqt5
```
To use matplotlib for drawing, you need to have it installed, e.g. with:
```bash
sudo pip3 install matplotlib
```

Note: If you have chosen manual installation, use `python3 dotplot` command to run the program (while in the `dotplot` directory) instead of sole `dotplot`.

### Basic usage

```bash
dotplot --fasta 1.fa 2.fa
```
To use graphical user interface, type: 

```bash
dotplot --fasta 1.fa 2.fa --gui
```

You can also fetch sequences from various sources (at once):
```bash
dotplot --gui --ncbi NP_001009852 --uniprot P03086
```

#### Advanced options

You can set window size to be used in plot creation:
```bash
dotplot --fasta 1.fa 2.fa --gui --window_size 2
```
Furthermore, you can combine it with stringency:
```bash
dotplot --fasta 1.fa 2.fa --gui --window_size 2 --stringency 2
```

And you can use a similarity matrix to compare aminoacids:
```bash
dotplot --fasta 1.fa 2.fa --gui --window_size 2 --stringency 2 --matrix PAM120
```

#### Getting help

To access list of available options run command above with added option `-h`.

## What will it do?
In the future our application will be able to read a wide range of input formats, and users will be able to parametrize alignment process and output format to their liking. 

## Dependencies & development
We are writing in `Python3` and strict on code styling, with pep8 and pylint validation. We require all code merging to master to have at least 7,5 pylint score. To check this, at first install pytlint with pip3 and then, run the following command: `python3 -m pylint dotplot.py`, where in place of `dotplot.py` use any name of the module to be tested. 
