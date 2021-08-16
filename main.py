import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)
from chess_game import game_start
import minimax as m
import time
from tkinter import *
from chess_board import make_board
from PIL import ImageTk,Image
from gui import *


game_start('self', 'minimax')







