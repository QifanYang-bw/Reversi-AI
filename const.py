from enum import Enum

class BoardState(Enum):
    Empty = 0
    Black = 1
    White = 2

class PlayerState(Enum):
	Human = 0
	AI = 1

n = 8
n_squared = n ** 2

AI_Search_Depth = 4
inf = int(1e5)
winning = int(1e4)

playerlist = [PlayerState.Human, PlayerState.AI]