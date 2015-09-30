__author__ = 'andrea'


class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.matrix = [['' for j in range(puzzle.rows)] for i in range(puzzle.cols)]
        self.used_pieces = []
        self.unused_pieces = list(self.puzzle.pieces)

    def next(self):
        matrix = [['' for j in range(puzzle.rows)] for i in range(puzzle.cols)]
        starting_position = (0,0)
        used_pieces = []
        unused_pieces = list(self.used_pieces)
        self.solve(matrix, starting_position, used_pieces, unused_pieces)

        # completed = False
        # pos = (0,0)
        # for piece in self.unused_pieces:
        #
        #     pos = self.get_next_free_position(pos)
        #
        #     for x_idx, row in enumerate(self.matrix):
        #         for y_idx, col in enumerate(row):
        #             if col == '':
        #
        #
        #
        # while not completed:
        #     if pos == (-1, -1) or len(self.unused_pieces) == 0:
        #         completed = True
        #
        #     for piece in self.unused_pieces:
        #     # piece = self.get_next_unused_piece()
        #     # if piece is not None:
        #         self.put_piece(piece, pos)
        #     # self.print_matrix(self.matrix)

    def solve(self, matrix, position, used_pieces, unused_pieces):

        if len(unused_pieces) == 0:
            return matrix





    def get_next_free_position(self, last_position):
        for x_idx, row in enumerate(last_position[0], self.matrix):
            for y_idx, col in enumerate(last_position[1], row):
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
        if len(self.unused_pieces) == 0:
            return None

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

    def is_on_border(self, position):
        for x in range(-1, 1):
            for y in range(-1, 1):
                if self.matrix[position[0] + x][position[1] + y] != '':
                    return True
        return False
