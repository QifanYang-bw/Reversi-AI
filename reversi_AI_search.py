""" reversi_AI_search.py

Contains the ReversiAI class.
"""

from enum import Enum
from random import random
from copy import deepcopy

from const import *
from core import *


class ReversiAI(object):
    """ReversiAI object that controls the move of AI.

    Attributes:
        __reversi: Reversi object.
        depth: int. The search depth of DFS.
        __currentState: BoardState object. The piece state of this AI.
        __opponentState: BoardState object. The piece state of this AI.
    """

    """
    The weight matrix is set according to position importance. The
    point on the edge are more crucial to take compared to the point
    in the middle, and the four positions on the corner are even more
    substantial: The pieces placed at the corner couldn't be flipped,
    and the pieces placed on the edge could only be flipped with other
    pieces on the same edge.
    """
    weight_matrix = [[16, 4, 4, 4, 4, 4, 4, 16],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [4, 1, 1, 1, 1, 1, 1, 4],
                     [16, 4, 4, 4, 4, 4, 4, 16]]
    def __init__(self, reversi, depth):
        self.__reversi = reversi
        self.depth = depth
        self.__currentState = None
        self.__opponentState = None

    def evaluate(self, condition):
        """ The evaluate function.

        The Score is evaluated as the sum of the position value
        (self as 1, opponent as -1) multiplied by the weight
        matrix value.
        """
        self_state = self.__currentState
        oppo_state = self.__opponentState
        score = 0

        for row in range(n):
            for col in range(n):
                cur_piece = condition.get_position_state(row, col)
                if cur_piece == self_state:
                    score += self.weight_matrix[row][col]
                elif cur_piece == oppo_state:
                    score -= self.weight_matrix[row][col]

        return score

    def alphabeta(self, condition, depth, alpha, beta):
        """ Alpha Beta Pruning based DFS.

        In the search process for possible moves, tree branches with
        solution better than other choices would be prevented by the
        opponent, and a move that is too bad would be prevented by
        us the AI. We save our best achievable result as alpha and
        the worse achievable result as beta, and filter out all moves
        that is smaller than alpha on our turn or moves that is larger
        than beta on our opponent's turn.
        """

        """ Returns the evaluation result when reaches maximum depth,
        or inf/-inf when a player wins.
        """

        if depth > self.depth:
            return (None, None, self.evaluate(condition))

        if condition.get_tot_chess_count() == n_squared:
            if condition.check_winning_status()[1] == self.__currentState:
                return (None, None, winning)
            if condition.check_winning_status()[1] == self.__opponentState:
                return (None, None, -winning)
            else:
                return (None, None, 0)

        """ Gather possible moves within an array. """

        branch = []
        new_condition = deepcopy(condition)

        for row in range(n):
            for col in range(n):
                try:
                    new_condition.move(row, col, safety_check=True)
                    branch.append(
                        (self.evaluate(new_condition), row, col, new_condition))

                    new_condition = deepcopy(condition)

                except BaseException:
                    pass

        best_row = None
        best_col = None

        if condition.get_current_state() == self.__currentState:
            """ Our turn """
            branch.sort(key=lambda element: -element[0])
            for child in branch:
                _, _, child_score = self.alphabeta(
                    child[3], depth + 1, alpha, beta)
                if child_score > alpha:
                    alpha = child_score
                    if beta <= alpha:
                        break
                    best_row = child[1]
                    best_col = child[2]
            if depth == 0 and best_col == None:
                raise Exception(
                    'None value detected for AI; ' + \
                    'The current branch info is' + \
                    map(lambda x:(x[1], x[2]), branch)
                )
            return (best_row, best_col, alpha)
        else:
            """ Our opponent's turn """
            branch.sort(key=lambda element: -element[0])
            for child in branch:
                _, _, child_score = self.alphabeta(
                    child[3], depth + 1, alpha, beta)
                if child_score < beta:
                    beta = child_score
                    if beta <= alpha:
                        break
                    best_row = child[1]
                    best_col = child[2]
            return (best_row, best_col, beta)

    def think(self):
        """ The main mathod for decision making."""
        self.__currentState = self.__reversi.get_current_state()
        self.__opponentState = self.__reversi.get_opponent_state()

        best_row, best_col, score = self.alphabeta(
            self.__reversi, 0, -inf, inf)

        print('AI   :', (best_row, best_col), 'Evaluation Score:', score)

        return best_row, best_col
