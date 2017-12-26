import pygame
from pygame.locals import *
from sys import exit

from const import *
from core import *
from interface import *

def player_status(currentColor, playerList):
	if currentColor == BoardState.Black:
		return playerList[0]
	elif currentColor == BoardState.White:
		return playerList[1]
	else:
		raise Exception('Unknown Color Status')

def Human_turn(reversi, interface):
	while True:
		event = pygame.event.wait()
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			try:
				interface.examine_and_move()
				print reversi.get_chess_count(), reversi.get_current_color()
				break
			except Exception as e:
				print e
	return

def AI_turn(reversi, interface):
	#(pos_row, pos_col) = Reversi_AI(reversi)

	#reversi.move(pos_row, pos_col, safety_check = True)
	pass

def main():
	reversi = Reversi()
	interface = ReversiInterface(reversi)
	interface.refresh()

	playerlist = [PlayerState.Human, PlayerState.Human]
	(Finished, Winner) = (False, None)

	while not Finished:
		current_player = player_status(reversi.get_current_color(), playerlist)

		if current_player == PlayerState.Human:
			Human_turn(reversi, interface)
		elif current_player == PlayerState.AI:
			AI_turn(reversi, interface)
		else:
			raise Exception('Unknown Player Status')

		interface.refresh()
		(Finished, Winner) = reversi.check_winning_status()

	interface.draw_winner(Winner)

	while True:
		event = pygame.event.wait()
		if event.type == QUIT:
			exit()
		else:
			interface.refresh()

# Check if main.py is the called program
if __name__ == '__main__':
	main()