""" core.py

Contains the Reversi core class.
"""

from enum import Enum
from copy import deepcopy
from const import *

pos_shift = [(-1, 0), (-1, 1), (0, 1), (1, 1),
             (1, 0), (1, -1), (0, -1), (-1, -1)]
initial_map = [[BoardState.Empty for j in range(n)] for i in range(n)]
for row in range(n // 2 - 1, n // 2 + 1):
    for col in range(n // 2 - 1, n // 2 + 1):
        if (row + col) & 1 == 0:
            initial_map[row][col] = BoardState.White
        else:
            initial_map[row][col] = BoardState.Black


class Reversi(object):
    """Reversi object that manages the entire game status.

    Attributes:
        __chessMap: 2-D List. the board status.
        __currentState: BoardState object`. the current active player.
        __BlackCount: int. the total number of black pieces.
        __WhiteCount: int. the total number of white pieces.
    """
    def __init__(
            self,
            chessMap=None,
            currentState=None,
            BlackCount=-1,
            WhiteCount=-1
    ):
        if chessMap is None:
            self.__chessMap = deepcopy(initial_map)
            self.__currentState = BoardState.Black
            self.__BlackCount = 2
            self.__WhiteCount = 2
        else:
            self.__set_board_state(
                chessMap,
                currentState,
                BlackCount,
                WhiteCount
            )

    def get_chessMap(self):
        """ Get the current 2-D board.
        For separation of concerns.

        Output:
            List object, represents the chess map in 2-D
        List.
        """
        return self.__chessMap

    def get_position_state(self, row, col):
        """ Get the state in a a specific.
        For separation of concerns.

        Output:
            BoardState object, represents the state in a
        specific position.
        """
        return self.__chessMap[row][col]

    def get_chess_count(self):
        """ Get the total number of chesses in black and white.
        For separation of concerns.

        Output:
            List object with 2 elements.
        """
        return (self.__BlackCount, self.__WhiteCount)

    def get_tot_chess_count(self):
        """ Get the total number of all chesses.
        Serves for separation of concerns, also as a quick check
        for game-ending condition.

        Output:
            Int object.
        """
        return self.__BlackCount + self.__WhiteCount

    def get_current_state(self):
        """ Get the current game player.
        For separation of concerns.

        Output:
            Int object.
        """
        return self.__currentState

    def get_reverse_state(self, chess):
        """ Get the reverse state of a certain state.
        Input:
            chess: BoardState object.
        Output:
            BoardState object.
        """
        if chess == BoardState.Black:
            return BoardState.White
        elif chess == BoardState.White:
            return BoardState.Black
        else:
            raise Exception('State is empty')

    def get_opponent_state(self):
        """ Get the player state that are not in action.

        Output:
            BoardState object.
        """
        return self.get_reverse_state(self.__currentState)

    def __set_board_state(self, chessMap, currentState,
                          BlackCount=-1, WhiteCount=-1):
        """Set the state when a chessMap is given. For convenience
        of Searching.

        Input:
            Same as self.__init__().
        """

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
        """Move the currentState to the other player."""
        self.__currentState = self.get_opponent_state()

    def position_test(self, pos_row, pos_col):
        """Check whether (pow_row, pos_col) is a valid position.

        Output:
            Bool object.
        """
        return pos_row >= 0 and \
               pos_row < n and \
               pos_col >= 0 and \
               pos_col < n

    def __extend(
            self,
            pos_row,
            pos_col,
            self_state,
            oppo_state,
            xshift,
            yshift
        ):

        """Check whether (pow_row, pos_col) is a valid position.

        Input:
            pos_row, pos_col: Position of the possible move position.
            self_state, oppo_state: BoardState objects.
            xshift, yshift: Shift vector.
        Output:
            Tuple object consisting of succeed status and flip.
        count.
        """
        count = 0
        flag = True
        if_succeed = False

        while flag:
            pos_row += xshift
            pos_col += yshift
            if self.position_test(pos_row, pos_col):
                if self.__chessMap[pos_row][pos_col] == oppo_state:
                    # Another piece to flip
                    count += 1
                elif self.__chessMap[pos_row][pos_col] == self_state:
                    # Connected with anchored piece, Success
                    if count > 0:
                        if_succeed = True
                    flag = False
                else:
                    # Failed to connect with anchored piece - Empty position
                    flag = False
            else:
                # Failed to connect with anchored piece - Out of board
                flag = False

        return (if_succeed, count)

    def __flip(self, pos_row, pos_col, self_state, oppo_state):
        """Flip the related pieces after the move.

        Input:
            pos_row, pos_col: Position of the possible move position.
            self_state, oppo_state: BoardState objects.
        Output:
            Tuple object consisting of change in counts for both sides.
        count.
        """
        flip_count = 0

        for (xshift, yshift) in pos_shift:
            (extend_success, extend_count) = self.__extend(
                pos_row, pos_col, self_state, oppo_state, xshift, yshift)
            if extend_success:
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

    def __next(self):
        """Switch the current State of player.
        """
        if self.check_availability(self.get_opponent_state()):
            self.__currentState = self.get_opponent_state()
        return

    def validity_test(self, pos_row, pos_col, self_state, oppo_state):
        """Test if the current State is valid.

        Output:
            Tuple object consists of success bool indicators and error
        message.
        """
        if not self.position_test(pos_row, pos_col):
            if pos_row < 0 or pos_row >= n:
                return (False, 'Row index out of range')
            if pos_col < 0 or pos_col >= n:
                return (False, 'Column index out of range')
        if self.__chessMap[pos_row][pos_col] != BoardState.Empty:
            return (False, 'Designated position is not empty')

        flag = False
        for (xshift, yshift) in pos_shift:
            (extend_success, extend_count) = self.__extend(
                pos_row, pos_col, self_state, oppo_state, xshift, yshift)
            if extend_success:
                flag = True
                break

        if flag:
            return (True, '')
        else:
            return (False, 'Invalid move')

    def move(self, pos_row, pos_col, safety_check=True):
        """Make a move on the board.

        Input:
            pos_row, pos_col: Position of the possible move position.
            safety_check: Bool object, indicate whether it is
        necessary to perform check beforehand. The parameter is given
        to boost performance.
        """
        oppo_state = self.get_opponent_state()

        if safety_check:
            if type(pos_row) != int or type(pos_col) != int:
                raise ValueError('Position data must be int')
            (valid, error_description) = self.validity_test(
                pos_row, pos_col, self.__currentState, oppo_state)
            if not valid:
                raise Exception(error_description)

        self.__chessMap[pos_row][pos_col] = self.__currentState
        if self.__currentState == BoardState.Black:
            self.__BlackCount += 1
        elif self.__currentState == BoardState.White:
            self.__WhiteCount += 1

        (black_count_shift, white_count_shift) = self.__flip(
            pos_row, pos_col, self.__currentState, oppo_state)
        self.__BlackCount += black_count_shift
        self.__WhiteCount += white_count_shift
        if self.__BlackCount < 0 or self.__WhiteCount < 0:
            raise ValueError('Negative Counter')

        self.__next()
        return

    #----------Status Check----------#
    def check_availability(self, self_state=None):
        """Output if there is any available position for current
        player on the board.

        Input:
            self_state: BoardState objects indicating the color of 
        piece for state checking. Default value is set to 
        self.__currentState.
        Output:
            Bool object.
        """
        if self_state is None:
            self_state = self.__currentState

        oppo_state = self.get_reverse_state(self_state)
        flag = False
        for row in range(n):
            for col in range(n):
                (valid, error_description) = self.validity_test(
                    row, 
                    col,
                    self_state,
                    oppo_state
                )
                if valid:
                    flag = True
                    break
            if flag:
                break
        return flag

    def check_winning_status(self):
        """Check the winner status.

        Output:
            Tuple object, consists of Bool indicator and the winnger in
        BoardState object.
        """
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

    def get_availability_map(self):
        """Returns the possible position for the current move.

        Cooperates with ReversiInterface.draw_availability_map().

        Output:
            2D List with available positions.
        """
        self_state = self.__currentState
        oppo_state = self.get_reverse_state(self_state)

        """
        The following line is faster than deepcopy().
        """
        ava_map = [[BoardState.Empty for j in range(n)] for i in range(n)]
        flag = False
        for row in range(n):
            for col in range(n):
                (valid, error_description) = self.validity_test(
                    row,
                    col,
                    self_state,
                    oppo_state
                )
                if valid:
                    ava_map[row][col] = self_state

        return ava_map
