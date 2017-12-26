import pygame
from pygame.locals import *
from const import *
from core import *

Image_Path = 'image/'

Left = 60
Top = 60
Right = 420
Bottom = 420

Width = Bottom - Top
Height = Right - Left

Grid_Size = Width / n
Piece_Size = 32

img_Width = 680
img_Height = 480

class ReversiInterface(object):

    def __init__(self, reversi):
        self.reversi = reversi

        # initialize pygame

        pygame.init()

        self.__screen = pygame.display.set_mode((img_Width, img_Height), 0, 32)
        pygame.display.set_caption('Othello')

        # load UI resources
        self.__img_chessboard = pygame.image.load(Image_Path + 'chessboard.png').convert()
        self.__img_piece_black = pygame.image.load(Image_Path + 'c_black.png').convert_alpha()
        self.__img_piece_white = pygame.image.load(Image_Path + 'c_white.png').convert_alpha()

    def transform_index2pixel(self, pos_row, pos_col):
        # Index to Coordinates
        return (Top + pos_col * Grid_Size, Left + pos_row * Grid_Size)

    def transform_pixel2index(self, x, y):
        # Coordinates to Index
        if x < Left or x >= Right or x < Top or x >= Bottom:
            return (None, None)

        (i, j) = (int((y - Top) / Grid_Size), int((x - Left) / Grid_Size))
        return (i, j)

    def refresh(self):
        # board
        self.__screen.blit(self.__img_chessboard, (0, 0))

        # chess piece
        for row in range(0, n):
            for col in range(0, n):
                state = self.reversi.get_position_state(row, col)

                if state != BoardState.Empty:
                    (x, y) = self.transform_index2pixel(row, col)
                    if state == BoardState.Black:
                        self.__screen.blit(self.__img_piece_black, (x, y))
                    elif state == BoardState.White:
                        self.__screen.blit(self.__img_piece_white, (x, y))

        pygame.display.update()

    #----------Interaction----------#
    def examine_and_move(self):
        mouse_button = pygame.mouse.get_pressed()
        if not mouse_button[0]:
            raise Exception('Not a Left Click')

        (x, y) = pygame.mouse.get_pos()
        (pos_row, pos_col) = self.transform_pixel2index(x, y)

        #print (x, y), (pos_row, pos_col)

        if pos_row == None:
            raise Exception('Out of Board Range')

        try:
            self.reversi.move(pos_row, pos_col, safety_check = True)
        except:
            raise
        
        return

    def draw_winner(self, result):
        font = pygame.font.SysFont('Arial', 55)
        tips = 'Game Over:'
        if result == BoardState.Black:
            tips = tips + 'Black Wins'
        elif result == BoardState.White:
            tips = tips + 'White Wins'
        else:
            tips = tips + 'Draw'
        text = font.render(tips, True, (240, 248, 255))

        self.__screen.blit(text, (img_Width / 2 - 200, img_Height / 2 - 50))

        pygame.display.update()









    # def draw_mouse(self):

    #     # track the mouse pointer
    #     (x, y) = pygame.mouse.get_pos()

    #     # chess piece moves with the mouse
    #     if self.__currentPieceState == BoardState.BLACK:
    #         self.__screen.blit(self.__ui_piece_black, (x - PIECE / 2, y
    #                            - PIECE / 2))
    #     else:
    #         self.__screen.blit(self.__ui_piece_white, (x - PIECE / 2, y
    #                            - PIECE / 2))

