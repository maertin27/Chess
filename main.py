import pieces
from Chessboard import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                        location_pieces, location_king, generate_all_moves, score_function)
from chess_game import game_start

board, count_moves = make_board()
board, count_moves = move_piece(board, coord('e8'), coord('e4'), count_moves)
loc_pieces = location_pieces(board)
loc_king = location_king(board, loc_pieces, 'b')
print_board(board)
print(pieces.total_check(loc_king, 'b', loc_pieces, board))
print(board[4][4].moves(board, loc_pieces, loc_king, count_moves))

game_start('random','random')





