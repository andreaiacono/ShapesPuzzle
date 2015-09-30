__author__ = 'andrea'

class Piece:
    def __init__(self, positions):
        self.positions = positions
        self.width = max(positions, key=lambda x: positions[1])
        self.height = max(positions, key=lambda x: positions[0])
        #print positions

    def flip(self):
        positions = []
        for position in self.positions:
            positions.append((self.height - position[0], position[1]))

        self.positions = positions

    def rotate(self):
        pass
