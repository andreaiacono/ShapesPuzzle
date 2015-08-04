__author__ = 'andrea'
import piece


class Puzzle:
    def __init__(self, filename):
        self.matrix = []
        self.placeholders = []
        self.rows = 0
        self.cols = 0
        self.pieces = []
        self.load(filename)

    def load(self, filename):
        self.rows = 0
        self.cols = 0
        self.matrix = [map(str, list(line.replace('\n', ''))) for line in open(filename, 'r') if line.strip() != '']

        for row in self.matrix:
            for col in row:
                if col not in self.placeholders:
                    self.pieces.append(self.get_new_piece(col))
                    self.placeholders.append(col)
                self.cols += 1
            self.rows += 1

    def get_new_piece(self, value):
        first_step = True
        piece_positions = []
        starting_position = 0,0
        for row_idx, row in enumerate(self.matrix):
            for col_idx, col in enumerate(row):
                if col == value:
                    if first_step:
                        starting_position = (row_idx, col_idx)
                        first_step = False
                    piece_positions.append((row_idx - starting_position[0], col_idx - starting_position[1]))

        self.pieces.append(piece.Piece(piece_positions))

    def get_model(self):
        return self.matrix

    def get_placeholders(self):
        return self.placeholders

    def get_color_index(self, element):
        for i in range(len(self.placeholders)):
            if element == self.placeholders[i]:
                return i
        return 0
