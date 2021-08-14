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
    def __init__(self, move, parent, score=0):
        self.move = move
        self.score = score
        self.children = []
        self.parent = parent

    def add_node(self, obj):
        self.children.append(obj)


def generate_tree(board, move_count, depth):
    color = 'b' if (move_count % 2) else 'w'
    loc_pieces = location_pieces(board)
    loc_king = location_king(board, loc_pieces, color)
    all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)
    move_count += 1

    tree = Tree(board)
    for moves in all_moves:
        for move in moves[1]:
            tree.add_node(Node([moves[0], move, move_count], tree))

    loopings(depth-1, tree)
    return tree


def generate_children(node, depth):
    # search moves to right position
    mvs = [node.move]
    n = node.parent
    while not isinstance(n, Tree):
        mvs.append(n.move)
        n = n.parent
    board = n.board

    # places the moves to the right position and determines which color's turn it is
    mvs.reverse()
    for mv in mvs:
        board = move_piece(board, mv[0], mv[1], mv[2])[0]
    move_count = mvs[-1][2] + 1
    color = 'w' if (move_count % 2) else 'b'
    # generate all moves from the position
    loc_pieces = location_pieces(board)
    loc_king = location_king(board, loc_pieces, color)
    if loc_king:
        all_moves = generate_all_moves(board, loc_pieces, color, loc_king, move_count)
        for moves in all_moves:
            for move in moves[1]:
                if depth == 1:
                    node.add_node(Node([moves[0], move, move_count], node, score_function(board, loc_pieces)))
                else:
                    node.add_node(Node([moves[0], move, move_count], node))
    else:
        node.score = -100 if color == 'w' else 100
    return node


def loopings(depth, root):
    for child in root.children:
        generate_children(child, depth)
        if depth - 1:
            loopings(depth - 1, child)

def minmax(node, depth,maximizing_player):
    if depth == 0 or node.children == []:
        return node.score
    if maximizing_player:
        value = -1000
        for child in node.children:
            value = max(value, minmax(child, depth-1, False))
    else:
        value = 1000
        for child in node.children:
            value = min(value, minmax(child, depth-1, True))
    return(value)

