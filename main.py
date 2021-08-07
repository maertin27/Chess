import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)
from chess_game import game_start

board, count_moves = make_board()
board, count_moves = move_piece(board, coord('e8'), coord('e4'), count_moves)
loc_pieces = location_pieces(board)
loc_king = location_king(board, loc_pieces, 'b')
print_board(board)
print(score_function(board, loc_pieces))
for i in range(50):
    game_start('random', 'random')




