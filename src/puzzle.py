__author__ = 'andrea'


class Puzzle():
    def __init__(self, filename):
        self.matrix = []
        self.placeholders = []
        self.rows = 0
        self.cols = 0
        self.load(filename)

    def load(self, filename):
        lines = open(filename)
        self.rows = 0
        self.cols = 0
        row_length = -1
        for line in lines:
            if row_length == -1:
                row_length = len(line) - 1

            if len(line) - 1 != row_length:
                print "ERROR: different lengths"
            if line[0] == '\n':
                continue
            row = []
            for col in line:
                if col == '\n':
                    continue
                row.append(col)
                if col not in self.placeholders:
                    self.placeholders.append(col)
            self.matrix.append(row)

        self.rows = len(self.matrix)
        print row_length
        print self.matrix

    def get_model(self):
        return self.matrix

    def get_placeholders(self):
        return self.placeholders

    def get_color_index(self, element):
        for i in range(len(self.placeholders)):
            if element == self.placeholders[i]:
                return i
        return 0

