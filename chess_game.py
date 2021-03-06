import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)
from random import randint
import minimax as m
from time import sleep
from random import sample
from gui import print_board2


def player_self(board, loc_pieces, loc_king, color, move_count,root):
    draw = False
    if color == 'w':
        colour = 'White'
    else:
        colour = 'Black'
    all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)
    if all_moves:
        moved = False
        while not moved:
            fro = coord(input(f'{colour}\'s turn, which piece do you want to move? \n> '))
            to = coord(input('Where or how do you want to move it? \n> '))
            for i, all_move in enumerate(all_moves):
                if fro in all_move and to in all_move[1]:
                    board, move_count = move_piece(board, fro, to, move_count)
                    print_board2(board, root)
                    moved = True
                    break
                if i == len(all_moves) - 1:
                    print('invalid move')
    else:
        draw = True
    return board, move_count, draw

def player_random(board, loc_pieces, loc_king, color, move_count,root):
    all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)
    draw = False
    if all_moves:
        r1 = randint(0, len(all_moves)-1)
        r2 = randint(0, len(all_moves[r1][1])-1)
        fro = all_moves[r1][0]
        to = all_moves[r1][1][r2]
        board, move_count = move_piece(board, fro, to, move_count)
        sleep(1)
        print_board2(board,root)
        print(move_count)
    else:
        draw = True
    return board, move_count, draw

def player_minimax(board, loc_pieces, loc_king, color, move_count,root):
    depth = 3
    tree = m.generate_tree(board, move_count, depth)
    best_score = m.minmax(tree, depth, True if color == 'w' else False)

    for i, child in sample(list(enumerate(tree.children)), len(tree.children)):
        if child.score == best_score:
            fro, to, z = tree.children[i].move
            break
    board, move_count = move_piece(board, fro, to, move_count)
    sleep(1)
    print_board2(board, root)
    print(move_count)
    draw = False
    return board, move_count, draw




def game_start(player_white, player_black):
    # possible players: self, random, minim ax
    board, move_count, root = make_board()
    print_board2(board, root)

    loc_king_white = True
    loc_king_black = True
    draw = False
    while loc_king_white and loc_king_black and not draw:

        #white turn
        color = 'w'
        colour = 'White'
        loc_pieces = location_pieces(board)
        loc_king_white = location_king(board, loc_pieces, color)
        if not loc_king_white:
            break
        if player_white == 'self':
            board, move_count, draw = player_self(board, loc_pieces, loc_king_white, color, move_count,root)

        if player_white == 'random':
            board, move_count, draw = player_random(board, loc_pieces, loc_king_white, color, move_count,root)
        if player_white == 'minimax':
            board, move_count, draw = player_minimax(board, loc_pieces, loc_king_white, color, move_count,root)
        if draw:
            break
        # black's turn
        color = 'b'
        loc_pieces = location_pieces(board)
        loc_king_black = location_king(board, loc_pieces, color)
        if not loc_king_black:
            break

        if player_black == 'self':
            board, move_count, draw = player_self(board, loc_pieces, loc_king_black, color, move_count,root)

        if player_black == 'random':
            board, move_count, draw = player_random(board, loc_pieces, loc_king_black, color, move_count,root)
        if player_black == 'minimax':
            board, move_count, draw = player_minimax(board, loc_pieces, loc_king_white, color, move_count,root)
        if draw:
            break

    if loc_king_white:
        print('Congratulations, white has won')
    elif loc_king_black:
        print('Congratulations, black has won')
    elif draw:
        print('This game ended in a draw')

