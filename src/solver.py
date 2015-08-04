__author__ = 'andrea'


class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.matrix = [['' for j in range(puzzle.rows)] for i in range(puzzle.cols)]
        self.used_pieces = []
        self.unused_pieces = list(self.puzzle.pieces)

    def next(self):
        completed = False
        while not completed:
            pos = self.get_next_free_position()
            if pos == (-1, -1):
                completed = True
            piece = self.get_next_unused_piece()
            self.put_piece(piece, pos)
            # self.print_matrix(self.matrix)

    def get_next_free_position(self):
        for x_idx, row in enumerate(self.matrix):
            for y_idx, col in enumerate(row):
                if col == '':
                    return x_idx, y_idx
        return -1, -1

    def get_next_free_symbol(self):
        symbols = ['0']
        for x_idx, row in enumerate(self.matrix):
            for y_idx, col in enumerate(row):
                if col != '' and col not in symbols:
                    symbols.append(col)
        print "symbols:" + str(symbols)
        return str(int(symbols[-1]) + 1)

    def get_next_unused_piece(self):
        piece = self.unused_pieces[0]
        self.unused_pieces.remove(piece)
        self.used_pieces.append(piece)
        return piece

    def put_piece(self, piece, pos):
        symbol = self.get_next_free_symbol()
        for element in piece.positions:
            self.matrix[pos[0] + element[0]][pos[1] + element[1]] = symbol

    def print_matrix(self, matrix):
        for row in matrix:
            for col in row:
                print col + " "
            print "\n"
