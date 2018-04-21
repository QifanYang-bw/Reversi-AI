""" Reversi-AI

A reversi game program with an implemented AI. Two players play on an 8x8
checker board using black and white pieces, starting from a 2x2 initial
state in the center. In each turn, the piece must be placed so that the
new piece and some occupied pieces forms a straight line, in which all
pieces are from the opponent. The opponent's piece in the middle of the
line will all be flipped to the other side. Player with the most pieces
on the board after the game ends wins.

Execution:
    ```bash
    $ cd Reversi-AI
    $ pip3 install -r requirement.txt
    $ python __main__.py
    ```

    within the folder or

    ```bash
    $ pip3 install -r Reversi-AI/requirement.txt
    $ python Reversi-AI
    ```

    outside to start the game.
    ```

See const.py for attribute list.
"""

import pygame
from pygame.locals import *
from sys import exit

from const import *
from core import *
from interface import *
from reversi_AI_search import *


def player_status(currentColor, playerList):
    """ Player Status Checking function.

    Returns the current player object given the board state and the
    Color(black/white) status.

    Input:
        currentColor: BoardState object. 
        playerList: List object, contains list of player property.

    Output:
        PlayerState object, either PlayerState.AI or PlayerState.Human 
    """

    if currentColor == BoardState.Black:
        return playerList[0]
    elif currentColor == BoardState.White:
        return playerList[1]
    else:
        raise Exception('Unknown Color Status')

def Human_turn(reversi, interface):
    """ Human_turn function with no output.

    Catch the current player move in interface object and react
    accordingly.

    Input:
        reversi: Reversi object.
        interface: ReversiInterface object.

    Output:
        None.
    """
    ava_map = None
    while True:

        interface.redraw()
        ava_map = interface.draw_availability_map(ava_map=ava_map)
        interface.draw_mouse_with_map(ava_map)
        interface.update()

        '''
        Catch the current player move.
        '''
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            try:
                '''
                Examine the validity of move and Move.
                '''
                row, col = interface.examine_and_move()
                print('Human:', (row, col))
                break
            except Exception as e:
                print('Human:', e)

    interface.redraw()
    interface.update()

    return

def AI_turn(Reversi_AI, interface):
    """ AI_turn function with no output.

    Make the move and display the move on the interface.

    Input:
        reversi: Reversi object.
        interface: ReversiInterface object.

    Output:
        None.
    """
    (pos_row, pos_col) = Reversi_AI.think()

    interface.reversi.move(pos_row, pos_col, safety_check=True)

    interface.redraw()
    interface.update()

    return


def main():
    """
    Initialization.
    """
    reversi = Reversi()
    interface = ReversiInterface(reversi)
    interface.redraw()
    interface.update()

    Reversi_AI = ReversiAI(reversi, depth=AI_Search_Depth)

    (Finished, Winner) = (False, None)

    """
    Loop until the game is finished.
    """
    while not Finished:
        """
        Retrieve current player status, since a player could move in
        two continuous rounds
        """
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

    """
    Draw the winner, Loop until the execution of quit command.
    """

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

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()
