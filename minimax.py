import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)


def generate_all_boards(board,all_moves,minmax_list):
    index = 0
    for i in range(len(all_moves)):
        for j in range(len(all_moves[i][1])):
            minmax_list[1][index], move = move_piece(board, all_moves[i][0], all_moves[i][1][j], 1)
            index += 1


def player_minimax(board, loc_pieces, loc_king, color, move_count, depth):
    all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)
    minmax_list = [board, all_moves]
    draw = False

    return board, move_count, draw

