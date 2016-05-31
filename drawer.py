class Drawer:

    def __init__(self, dot_matrix=[]):

        self.dot_matrix = dot_matrix
        pass

    def get_matrix(self):

        return self.dot_matrix

    def set_matrix(self, new_matrix):

        self.dot_matrix = new_matrix

    def draw(self):
        drawing = ""

        for row in self.dot_matrix:

            for element in row:

                if element == 1:
                    drawing = drawing + "."
                else:
                    drawing = drawing + " "

        return drawing
