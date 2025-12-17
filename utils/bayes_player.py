import copy
import math
import OthelloLogic
import numpy as np
from utils import alpha_beta_search

BETA_CANDIDATES = [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.2]

DEPTH = 1

class BayesPlayer:
    def update_opponent_model(self, prev_board: list[list[int]], move: list[int], opponent_model: list[float], evaluate_func):
        """
        相手の強さのモデルを更新する
        
        :param prev_board: ひとつ前の盤面
        :type prev_board: list[list[int]]
        :param move: 相手がとった手
        :type move: list[int]
        :param opponent_model: 相手の強さのモデル
        :type opponent_model: list[float]
        """
        # 合法手を取得
        candidate_moves:list[list[int]] = OthelloLogic.getMoves(prev_board, -1, len(prev_board))
        
        move_index: int | None = None

        for i in range(len(candidate_moves)):
            if candidate_moves[i] == move:
                move_index = i
                break
        
        if move_index is None:
            return opponent_model

        # 尤度のリスト
        likelihood = []

        for i in range(len(BETA_CANDIDATES)):
            beta = BETA_CANDIDATES[i]
            # 特定のβに対する確率分布
            probabilities:np.ndarray = self.get_moves_probabilities(candidate_moves, prev_board, beta, evaluate_func)
            # 実際に打たれた手の尤度を記録
            likelihood.append(probabilities[move_index])
        

        # 周辺確率
        marginal_probability = 0
        for i in range(len(BETA_CANDIDATES)):
            marginal_probability += likelihood[i] * opponent_model[i]
        
        # 0除算を避ける
        if marginal_probability == 0:
            return opponent_model

        # 新しいモデル
        new_opponent_model = []

        
        for i in range(len(BETA_CANDIDATES)):
            # ベイズの定理を用いて計算
            posterior_probability = likelihood[i] / marginal_probability * opponent_model[i]
            new_opponent_model.append(posterior_probability)

        return new_opponent_model

    def get_moves_predict(self, moves:list[list[int]], board:list[list[int]], opponent_model: list[float], evaluate_func):
        """
        それぞれの手を打つ可能性を求める関数
        
        :param moves: 合法手のリスト
        :type moves: list[list[int]]
        :param board: 現在の盤面
        :type board: list[list[int]]
        :param opponent_model: 現在の相手のモデル
        :type opponent_model: list[float]
        """
        predict = np.zeros(len(moves))
        for i in range(len(BETA_CANDIDATES)):
            beta = BETA_CANDIDATES[i]
            confidence_score = opponent_model[i]
            probabilities:np.ndarray = self.get_moves_probabilities(moves, board, beta, evaluate_func)
            predict = predict + probabilities * confidence_score
        return  predict.tolist()

    def get_moves_probabilities(self, moves:list[list[int]], board:list[list[int]], beta:float, evaluate_func):
        """
        相手の強さをβと仮定したときの各手を打ちうる確率
        
        :param moves: 合法手のリスト
        :type moves: list[list[int]]
        :param board: 現在の盤面
        :type board: list[list[int]]
        :param beta: 相手の強さβ
        :type beta: float
        """
        preferences:list[float] = []
        mobility = len(moves)
        for move in moves:
            expect_board = OthelloLogic.execute(copy.deepcopy(board), move, -1, len(board))
            preference = self.get_move_preference(move, expect_board, beta, evaluate_func, mobility) # type: ignore
            preferences.append(preference)
        # softmax関数で確率密度に変換
        probabilities:np.ndarray = softmax(np.array(preferences))
        return probabilities

    def get_move_preference(self, move:list[int], board: list[list[int]], beta: float, evaluate_func, mobility):
        """
        ある手に対してその手を打つ可能性
        
        :param move: 手
        :type move: list[list[int]]
        :param board: 盤面
        :type board: list[list[int]]
        :param beta: 相手の強さβ
        :type beta: float
        """
        
        a = - math.inf
        b = math.inf

        score = alpha_beta_search.alpha_beta_search(copy.deepcopy(board), DEPTH, a, b, False, -1, evaluate_func)
        preference = score * beta
        return preference

def softmax(x: np.ndarray):
    # NaN や inf を除去
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)

    # 最大値を引いてオーバーフロー防止
    max_x = np.max(x)
    exp_x = np.exp(x - max_x)

    sum_exp = np.sum(exp_x)

    # 全部0なら一様分布にする
    if sum_exp == 0:
        return np.ones(len(x)) / len(x)

    return exp_x / sum_exp
