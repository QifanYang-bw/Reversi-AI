from enum import Enum
from copy import deepcopy
from const import *

pos_shift = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
initial_map = [[BoardState.Empty for j in range(n)] for i in range(n)]
for row in range(n // 2 - 1, n // 2 + 1):
	for col in range(n // 2 - 1, n // 2 + 1):
		if (row + col) & 1 == 0:
			initial_map[row][col] = BoardState.White
		else:
			initial_map[row][col] = BoardState.Black

# a = BoardState.Black
# b = BoardState.White
# c = BoardState.Empty
# initial_Map       = [[a, a, a, a, a, a, a, c],
# 					 [a, a, a, a, b, b, b, c],
# 					 [a, a, a, a, a, a, a, a],
# 					 [a, a, a, a, a, a, a, c],
# 					 [a, b, a, a, a, a, a, a],
# 					 [a, a, a, a, a, a, a, c],
# 					 [a, a, a, a, a, a, c, c],
# 					 [a, a, a, a, a, a, a, a]]

class Reversi(object):
	#----------Initialization----------#
	def __init__(self, chessMap = None, currentState = None, BlackCount = -1, WhiteCount = -1):
		if chessMap == None:
			self.__chessMap = deepcopy(initial_map)
			self.__currentState = BoardState.Black
			self.__BlackCount = 2
			self.__WhiteCount = 2
		else:
			self.__set_board_state(chessMap, currentState, BlackCount, WhiteCount)

	def get_chessMap(self):
		return self.__chessMap

	def get_position_state(self, row, col):
		return self.__chessMap[row][col]

	def get_chess_count(self):
		return (self.__BlackCount, self.__WhiteCount)

	def get_tot_chess_count(self):
		# Serves as a quick check for winning condition
		return self.__BlackCount + self.__WhiteCount

	def get_current_state(self):
		return self.__currentState

	def get_reverse_state(self, chess):
		if chess == BoardState.Black:
			return BoardState.White
		elif chess == BoardState.White:
			return BoardState.Black
		else:
			raise Exception('State is empty')

	def get_opponent_state(self):
		return self.get_reverse_state(self.__currentState)

	def __set_board_state(self, chessMap, currentState,
						BlackCount = -1, WhiteCount = -1):
		if len(chessMap) != n or len(chessMap[0]) != n:
			raise Exception('Board dimension mismatch: expected', 
							'(' + str(n) + ',' + str(n) + ')')
		if BlackCount == -1 or WhiteCount == -1:
			BlackCount = 0
			WhiteCount = 0
			for row in range(n):
				for col in range(n):
					if chessMap[row][col] == BoardState.Black:
						BlackCount += 1
					elif chessMap[row][col] == BoardState.White:
						WhiteCount += 1

		self.__chessMap = chessMap
		self.__BlackCount = BlackCount
		self.__WhiteCount = WhiteCount
		self.__currentState = currentState

	def swap_state(self):
		self.__currentState = self.get_opponent_state()

	#----------Move----------#
	def position_test(self, pos_row, pos_col):
		return pos_row >= 0 and pos_row < n and pos_col >= 0 and pos_col < n

	def __extend(self, pos_row, pos_col, self_state, oppo_state, xshift, yshift):
		count = 0
		flag = True
		if_succeed = False

		while flag:
			pos_row += xshift
			pos_col += yshift
			if self.position_test(pos_row, pos_col):
				if self.__chessMap[pos_row][pos_col] == oppo_state:
					#Another piece to flip
					count += 1
				elif self.__chessMap[pos_row][pos_col] == self_state:
					#Connected with anchored piece, Success
					if count > 0:
						if_succeed = True
					flag = False
				else:
					#Failed to connect with anchored piece - Empty position
					flag = False
			else:
				#Failed to connect with anchored piece - Out of board
				flag = False

		#print pos_row, pos_col, (if_succeed, count)
		#if pos_row == 2 and pos_col == 2:
			#print (if_succeed, count)
		return (if_succeed, count)

	def __flip(self, pos_row, pos_col, self_state, oppo_state):
		flip_count = 0

		for (xshift, yshift) in pos_shift:
			(extend_success, extend_count) = self.__extend(pos_row, pos_col, self_state, oppo_state, xshift, yshift)
			if extend_success:
				#print (xshift, yshift), (extend_success, extend_count)
				new_row = pos_row
				new_col = pos_col
				for counter in range(extend_count):
					new_row += xshift
					new_col += yshift
					self.__chessMap[new_row][new_col] = self_state
				flip_count += extend_count

		if self_state == BoardState.Black:
			return (flip_count, -flip_count)
		elif self_state == BoardState.White:
			return (-flip_count, flip_count)
		raise ValueError('Unknown Board State')

	def __switch(self, self_state, oppo_state):
		if self.check_availability(oppo_state):
			self.__currentState = oppo_state
		else:
			self.__currentState = self_state
		return

	def validity_test(self, pos_row, pos_col, self_state, oppo_state):
		if not self.position_test(pos_row, pos_col):
			if pos_row < 0 or pos_row >= n:
				return (False, 'Row index out of range')
			if pos_col < 0 or pos_col >= n:
				return (False, 'Column index out of range')
		if self.__chessMap[pos_row][pos_col] != BoardState.Empty:
			return (False, 'Designated position is not empty')

		flag = False
		for (xshift, yshift) in pos_shift:
			(extend_success, extend_count) = self.__extend(pos_row, pos_col, self_state, oppo_state, xshift, yshift)
			if extend_success:
				flag = True
				break

		if flag:
			return (True, '')
		else:
			return (False, 'Invalid move')

	def move(self, pos_row, pos_col, safety_check = True):
		oppo_state = self.get_opponent_state()

		if safety_check:
			(valid, error_description) = self.validity_test(pos_row, pos_col, self.__currentState, oppo_state)
			if not valid:
				raise Exception(error_description)

		self.__chessMap[pos_row][pos_col] = self.__currentState
		if self.__currentState == BoardState.Black:
			self.__BlackCount += 1
		elif self.__currentState == BoardState.White:
			self.__WhiteCount += 1

		(black_count_shift, white_count_shift) = self.__flip(pos_row, pos_col, self.__currentState, oppo_state)
		#print (black_count_shift, white_count_shift)
		self.__BlackCount += black_count_shift
		self.__WhiteCount += white_count_shift
		if self.__BlackCount < 0 or self.__WhiteCount < 0:
			raise Exception('Negative Counter')

		self.__switch(self.__currentState, oppo_state)
		return

	#----------Status Check----------#
	def check_availability(self, self_state = None):
		if self_state == None:
			self_state = self.__currentState

		#Could be optimized
		oppo_state = self.get_reverse_state(self_state)
		flag = False
		for row in range(n):
			for col in range(n):
				(valid, error_description) = self.validity_test(row, col, self_state, oppo_state)
				#sprint row, col, (valid, error_description)
				if valid:
					flag = True
					break
			if flag: break
		return flag

	def check_winning_status(self):
		Finished = False
		Winner = None

		if self.__BlackCount + self.__WhiteCount == n_squared:
			Finished = True
		elif not self.check_availability() and not self.check_availability(self.get_opponent_state()):
			Finished = True

		if Finished:
			if self.__BlackCount > self.__WhiteCount:
				Winner = BoardState.Black
			elif self.__BlackCount < self.__WhiteCount:
				Winner = BoardState.White
			else:
				Winner = BoardState.Empty

		return (Finished, Winner)

