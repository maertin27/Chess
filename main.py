import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)
from chess_game import game_start
import minimax as m
import time

board, move_count = make_board()
print_board(board)


start_time = time.time()
tree = m.generate_tree(board, move_count, 3)
print("--- %s seconds ---" % (time.time() - start_time))

print(tree.children[0].children[0].children[0].move)








