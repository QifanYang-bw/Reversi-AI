import pygame
from pygame.locals import *
from sys import exit

from const import *
from core import *
from interface import *
from reversi_AI_search import *


def player_status(currentColor, playerList):
    if currentColor == BoardState.Black:
        return playerList[0]
    elif currentColor == BoardState.White:
        return playerList[1]
    else:
        raise Exception('Unknown Color Status')

# Could be rewritten as class structure


def Human_turn(reversi, interface):
    ava_map = None
    while True:
        interface.redraw()
        ava_map = interface.draw_availability_map(ava_map=ava_map)
        interface.draw_mouse_with_map(ava_map)
        interface.update()

        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            try:
                row, col = interface.examine_and_move()
                print('Human:', (row, col))
                break
            except Exception as e:
                print('Human:', e)

    interface.redraw()
    interface.update()

    return


def AI_turn(Reversi_AI, interface):
    (pos_row, pos_col) = Reversi_AI.think()

    interface.reversi.move(pos_row, pos_col, safety_check=True)

    interface.redraw()
    interface.update()

    return


def main():
    reversi = Reversi()
    interface = ReversiInterface(reversi)
    interface.redraw()
    interface.update()

    Reversi_AI = ReversiAI(reversi, depth=AI_Search_Depth)

    (Finished, Winner) = (False, None)

    while not Finished:
        current_player = player_status(reversi.get_current_state(), playerlist)

        print('\nState:', reversi.get_current_state())

        if current_player == PlayerState.Human:
            Human_turn(reversi, interface)
        elif current_player == PlayerState.AI:
            AI_turn(Reversi_AI, interface)
        else:
            raise Exception('Unknown Player Status')

        print('(Black, White):', reversi.get_chess_count())

        (Finished, Winner) = reversi.check_winning_status()

    interface.draw_winner(Winner)
    interface.update()

    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        else:
            interface.redraw()
            interface.draw_winner(Winner)
            interface.update()


# Check if main.py is the called program
if __name__ == '__main__':
    main()
