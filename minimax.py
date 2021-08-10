import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)


def generate_tree(board, depth):
    # this tree will have recursive structure
    # all_pos_moves = [[fro,to,score,[all_pos_moves]],[fro,to,score,[all_pos_moves]], ...]
    for i in







