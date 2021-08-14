import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)
from chess_game import game_start
import minimax as m
import time

board, move_count = make_board()
board, move_count = move_piece(board,coord('e1'),coord('e5)'),move_count)
print_board(board)


start_time = time.time()
tree = m.generate_tree(board, move_count, 4)
print("--- %s seconds ---" % (time.time() - start_time))

print(tree.children[0].move)
print(tree.children[0].score)
print(tree.children[0].children[0].move)
print(tree.children[0].children[0].score)
#print(tree.children[0].children[0].children[0].move)
#print(tree.children[0].children[0].children[0].score)
#print(tree.children[0].children[0].children[0].children[0].move)
#print(tree.children[0].children[0].children[0].children[0].score)

start_time = time.time()
print(m.minmax(tree, 4, True))
print("--- %s seconds ---" % (time.time() - start_time))







