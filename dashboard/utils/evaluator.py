from utils import OthelloLogic

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
        score = 0
        for x in range(8):
            for y in range(8):
                score += board[x][y] * self.weights[x][y] * color
        return score
    def calc_confirmed_stones(self, board, color):
        score = 0
        if board[0][0] == color:
            score += 1
        elif board[0][0] == -color:
            score -= 1
        
        if board[7][0] == color:
            score += 1
        elif board[7][0] == -color:
            score -= 1
        
        if board[0][7] == color:
            score += 1
        elif board[0][7] == -color:
            score -= 1
        
        if board[7][7] == color:
            score += 1
        elif board[7][7] == -color:
            score -= 1
        
        return score


    def evaluate(self, board, color):
        moves = OthelloLogic.getMoves(board, color, len(board))
        mobility = len(moves)
        bp = self.calc_board_position(board, color)
        cs = self.calc_confirmed_stones(board, color)
        score = bp * 1 + cs * 10 + mobility * 2
        return (score + 1100) / 2200 * 100
        
