import pieces
from chess_board import (make_board, move_piece, castling, en_passant, print_board, coord, dictionary,
                         location_pieces, location_king, generate_all_moves, score_function)


# tree
class Tree:
    def __init__(self, board):
        self.children = []
        self.board = board

    def add_node(self, obj):
        self.children.append(obj)


class Node:
    def __init__(self, fro, to):
        self.fro = fro
        self.to = to
        self.score = 0
        self.children = []
        self.parent = parent

    def add_node(self, obj):
        self.children.append(obj)


def generate_tree(board, depth):
    color = 'w'
    move_count = 0
    loc_pieces = location_pieces(board)
    loc_king = location_king(board, loc_pieces, color)
    all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)

    tree = Tree(board)
    for moves in all_moves:
        for move in moves[1]:
            tree.add_node(Node(moves[0], move))
    return tree

def generate_children(node,)


