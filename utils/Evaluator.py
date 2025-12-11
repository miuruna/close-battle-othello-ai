POSITION_TABLE = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 0, 0, 0, 0, -2, 10],
    [5, -2, 0, 0, 0, 0, -2, 5],
    [5, -2, 0, 0, 0, 0, -2, 5],
    [10, -2, 0, 0, 0, 0, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

class Evaluator:
    def __init__(self):
        self.weights = POSITION_TABLE
        
    def calc_board_position(self, board, color):
        pass

    def calc_confirmed_stones(self, board, color):
        pass

    def calc_mobility(self, board, color):
        pass

    def evaluate(self, board, color):
        bp = self.calc_board_position(board, color)
        cs = self.calc_confirmed_stones(board, color)
        nc = self.calc_mobility(board, color)

        return bp * 1 + cs * 10 + nc * 2
        
