from enum import Enum
from random import random
from copy import deepcopy

from const import *
from core import *

class ReversiAI(object):
	weight_matrix = [[52, 10, 8, 8, 8, 8, 10, 52],
					 [10, 2,  2, 2, 2, 2, 2,  10],
					 [8,  2,  2, 1, 1, 2, 2,  8],
					 [8,  2,  1, 2, 2, 1, 2,  8],
					 [8,  2,  1, 2, 2, 1, 2,  8],
					 [8,  2,  2, 1, 1, 2, 2,  8],
					 [10, 2,  2, 2, 2, 2, 2,  10],
					 [52, 10, 8, 8, 8, 8, 10, 52]]
	__currentState = None
	__opponentState = None

	def __init__(self, reversi, depth):
		self.__reversi = reversi
		self.depth = depth

	def evaluate(self, condition):
		self_state = condition.get_current_state()
		oppo_state = condition.get_opponent_state()
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
		if depth > self.depth:
			return (None, None, self.evaluate(condition))

		if condition.get_tot_chess_count() == n_squared:
			if condition.check_winning_status()[1] == self.__currentState:
				return (None, None, winning)
			if condition.check_winning_status()[1] == self.__opponentState:
				return (None, None, -winning)
			else:
				return (None, None, 0)

		branch = []
		new_condition = deepcopy(condition)
		#print depth, condition.get_chess_count()

		for row in range(n):
			for col in range(n):
				try:
					new_condition.move(row, col, safety_check = True)
					branch.append((self.evaluate(new_condition), row, col, new_condition))

					new_condition = deepcopy(condition)
					#print depth, condition.get_chess_count()

				except:
					pass

		best_row = None
		best_col = None

		if condition.get_current_state() == self.__currentState:
			branch.sort(key = lambda element:-element[0])
			best_score = -inf
			for child in branch:
				_, _, child_score = self.alphabeta(child[3], depth + 1, alpha, beta)
				if child_score > best_score:
					best_score = child_score
					best_row = child[1]
					best_col = child[2]
					if best_score > alpha:
						alpha = best_score
						if beta <= alpha:
							break
		else:
			branch.sort(key = lambda element:-element[0])
			best_score = inf
			for child in branch:
				_, _, child_score = self.alphabeta(child[3], depth + 1, alpha, beta)
				if child_score < best_score:
					best_score = child_score
					best_row = child[1]
					best_col = child[2]
					if best_score < beta:
						beta = best_score
						if beta <= alpha:
							break

		return (best_row, best_col, best_score)

	def think(self):
		self.__currentState = self.__reversi.get_current_state()
		self.__opponentState = self.__reversi.get_opponent_state()
		print self.__currentState, self.__opponentState

		best_row, best_col, score = self.alphabeta(self.__reversi, 0, -inf, inf)

		print 'AI   :', (best_row, best_col), 'Evaluation Score:', score

		return best_row, best_col

