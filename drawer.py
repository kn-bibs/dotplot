class Drawer(object):

    def __init__(self):
        pass


    def draw(self, dot_matrix):

        for row in dot_matrix:
            for element in row:
                if element == 1:
                    print("x")
                else:
                    print(" ")
            print("\n")

