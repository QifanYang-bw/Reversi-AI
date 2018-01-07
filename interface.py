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
        self.__img_piece_hint = pygame.image.load(Image_Path + 'c_hint.png').convert_alpha()

    #----------Modules----------#
    # Source for blit_alpha: http://www.nerdparadise.com/programming/pygameblitopacity
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

    def transform_index2pixel(self, pos_row, pos_col):
        # Index to Coordinates
        return (Top + pos_col * Grid_Size, Left + pos_row * Grid_Size)

    def transform_pixel2index(self, x, y):
        # Coordinates to Index
        if x < Left or x >= Right or y < Top or y >= Bottom:
            return (None, None)

        (i, j) = (int((y - Top) / Grid_Size), int((x - Left) / Grid_Size))
        return (i, j)

    def redraw(self):
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

        font = pygame.font.SysFont('Consolas', 44)
        cur_black, cur_white = self.reversi.get_chess_count();

        text = font.render(str(cur_black).zfill(2), True, (27, 27, 27))
        pygame.draw.circle(self.__screen, (27, 27, 27), (525, 83), 20)
        pygame.draw.circle(self.__screen, (64, 64, 64), (525, 83), 20, 2)
        self.__screen.blit(text, (574, 69))

        text = font.render(str(cur_white).zfill(2), True, (236, 236, 236))
        pygame.draw.circle(self.__screen, (244, 255, 250), (525, 173), 20)
        pygame.draw.circle(self.__screen, (188, 194, 192), (525, 173), 20, 2)
        self.__screen.blit(text, (574, 159))

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()

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
        
        return (pos_row, pos_col)

    def draw_winner(self, result):
        font = pygame.font.SysFont('Arial', 55)
        tips = 'Game Over:'
        if result == BoardState.Black:
            tips = tips + 'Black Wins'
        elif result == BoardState.White:
            tips = tips + 'White Wins'
        else:
            tips = tips + 'Draw'
        text = font.render(tips, True, (142, 202, 255))

        self.__screen.blit(text, (img_Width / 2 - 200, img_Height / 2 - 50))

    def draw_mouse_with_map(self, ava_map):

        #----------Check the position of pointer----------#
        (x, y) = pygame.mouse.get_pos()
        (pos_row, pos_col) = self.transform_pixel2index(x, y)
        if pos_row == None: return
        #print (pos_row, pos_col)

        self_state = self.reversi.get_current_state()

        if ava_map[pos_row][pos_col] == self_state:
            (out_x, out_y) = self.transform_index2pixel(pos_row, pos_col)
            if self.reversi.get_current_state() == BoardState.Black:
                self.blit_alpha(self.__screen, self.__img_piece_black, 
                                (out_x, out_y),
                                128)
            else:
                self.blit_alpha(self.__screen, self.__img_piece_white, 
                                (out_x, out_y),
                                128)

    def draw_availability_map(self, ava_map = None):
        self_state = self.reversi.get_current_state()
        if ava_map == None:
            ava_map = self.reversi.get_availability_map()

        for row in range(0, n):
            for col in range(0, n):
                if ava_map[row][col] == self_state:
                    (x, y) = self.transform_index2pixel(row, col)
                    self.__screen.blit(self.__img_piece_hint, (x + 1, y + 2))

        return ava_map


