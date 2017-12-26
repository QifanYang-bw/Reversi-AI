from enum import Enum

n = 8
n_squared = n * n

class BoardState(Enum):
    Empty = 0
    Black = 1
    White = 2

class PlayerState(Enum):
	Human = 0
	AI = 1
