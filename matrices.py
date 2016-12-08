"""This module works with similarity matrices of aminoacids"""


def read_matrix(name):
    """This function converts the matrix into a dictionary"""
    with open("matrices/" + name + ".txt") as f:
        lines = f.readlines()
        matrix = {}
        aa_list = lines[0].split()
        for i in aa_list:
            matrix[i] = {}
        for line in lines[1:]:
            data = line.split()
            name = data[0]
            values = data[1:]
            matrix[name] = dict(zip(aa_list, values))


def read_pair(matrix, a, b):
    """This function returns similarity values for 2 aminoacids"""
    return (matrix[a])[b]
