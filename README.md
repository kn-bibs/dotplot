# Dotplot


## Idea

Dotplot is a plot used mainly in biology for graphical visualisations of sequences' similarity. [Read more on Wikipedia] (https://en.wikipedia.org/wiki/Dot_plot_%28bioinformatics%29)

## Why to create a new package?

There are many programs that attempt to create dotplots already. Unfortunately most of these programs was created long time ago and written in old versions of Java. To allow new generations of bioinformaticians to generate dotplots easily we are developing this Python3 package.

## Installation & usage
``git clone https://github.com/kn-bibs/dotplot``


###Basic usage

``cd dotplot``

``python3 dotplot.py --file1 seq1.fasta --file2 seq2.fasta``

## What will it do?
In the future our application will be able to read a wide range of input formats, and users will be able to parametrize alignment process and output format to their liking. 

## Dependencies & development
We are writing in `Python3` and strict on code styling, with pep8 and pylint validation. We require all code merging to master to have at least 7,5 pylint score.