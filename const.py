import os

from enum import Enum
class BoardState(Enum):
    Empty = 0
    Black = 1
    White = 2


class PlayerState(Enum):
    Human = 0
    AI = 1


dirname = os.path.dirname(__file__)

n = 8
n_squared = n ** 2

AI_Search_Depth = 3
inf = int(1e8)
winning = int(1e4)

playerlist = [PlayerState.Human, PlayerState.AI]
