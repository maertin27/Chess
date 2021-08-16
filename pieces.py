from numpy import array
from chess_board import move_piece, location_pieces
import tkinter as tk

def outside_board(loc):
    # checks if given coordinates are inside the borders of the board
    return 0 > loc[0] or 7 < loc[0] or 0 > loc[1] or 7 < loc[1]


def piece_in_loc(loc, loc_pieces):
    # checks if a piece is located at given coordinates
    bool_list = []
    for loc_piece in loc_pieces:
        bool_list.append(loc == [loc_piece[0], loc_piece[1]])

    return bool_list


def valid_move(new_loc, loc_pieces, color, list_moves):
    loop = True
    if 0 > new_loc[0] or 7 < new_loc[0] or 0 > new_loc[1] or 7 < new_loc[1]:
        loop = False
    else:
        bool_list = piece_in_loc(new_loc, loc_pieces)
        if any(bool_list):
            loop = False
            if color != array(loc_pieces)[array(bool_list)].tolist()[0][2]:
                list_moves.append(new_loc)
        else:
            list_moves.append(new_loc)
    return list_moves, loop


def check(new_loc, loc_pieces, attackers, board, color_king):
    loop = True
    chec = False
    if 0 > new_loc[0] or 7 < new_loc[0] or 0 > new_loc[1] or 7 < new_loc[1]:
        loop = False
    else:
        bool_list = piece_in_loc(new_loc, loc_pieces)
        if any(bool_list):
            loop = False
            if color_king != array(loc_pieces)[array(bool_list)].tolist()[0][2]:
                b_list = []
                for attacker in attackers:
                    b_list.append(type(board[new_loc[0]][new_loc[1]]).__name__ == attacker)
                    if any(b_list):
                        chec = True
    return chec, loop


def total_check(loc_king, color_king, loc_pieces, board):
    chec = False
    # rook and queen
    attackers = ['Rook', 'Queen']
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for x, y in moves:
        loc = loc_king
        loop = True
        while loop:
            new_loc = [loc[0] + x, loc[1] + y]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        if chec:
            break

    # bishop and queen
    if not chec:
        attackers = ['Bishop', 'Queen']
        moves = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        for x, y in moves:
            loc = loc_king
            loop = True
            while loop:
                new_loc = [loc[0] + x, loc[1] + y]
                chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
                loc = new_loc
            if chec:
                break

    # knight
    if not chec:
        attackers = ['Knight']
        knightmoves = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [2, -1], [1, -2], [2, 1], [1, 2]]
        for move in knightmoves:
            new_loc = [loc_king[0] + move[0], loc_king[1] + move[1]]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break
    # pawn
    if not chec:
        attackers = ['Pawn']
        direction = -1 if color_king == 'w' else 1
        locs = [[loc_king[0]+direction, loc_king[1]-1], [loc_king[0]+direction, loc_king[1]+1]]
        for loc in locs:
            chec, loop = check(loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break

    # king
    if not chec:
        attackers = ['King']
        kingmoves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, -1]]
        for kingmove in kingmoves:
            new_loc = [loc_king[0] + kingmove[0], loc_king[1] + kingmove[1]]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break

    return chec


def remove_moves_check(loc, color, list_moves, board, loc_king):
    list_moves2 = []
    for move in list_moves:
        board2, count = move_piece(board, loc, move, 0)
        loc_pieces2 = location_pieces(board2)
        chec = total_check(loc_king, color, loc_pieces2, board2)
        if not chec:
            list_moves2.append(move)
    return list_moves2


class Piece:
    def __init__(self, loc, color):
        self.loc = loc
        self.color = color
        self.moved = 0


class King(Piece):

    def __str__(self):
        return '\u265A' if self.color == 'w' else '\u2654'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        king_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        loc = self.loc
        color = self.color
        moved = self.moved
        # generating possible moves
        for king_move in king_moves:
            new_loc = [loc[0] + king_move[0], loc[1] + king_move[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, color, list_moves)
        # removing moves that lead to checks
        list_moves2 = []
        for move in list_moves:
            chec = total_check(move, color, loc_pieces, board)
            if not chec:
                list_moves2.append(move)
        # castling
        if moved == 0:
            if color == 'w':
                x = 7
                c = 'w'
            else:
                x = 0
                c = 'b'
                # right castling
            if (not any(piece_in_loc([x, 5], loc_pieces)) and
                not any(piece_in_loc([x, 6], loc_pieces)) and
                not total_check([x, 4], c, loc_pieces, board) and
                not total_check([x, 5], c, loc_pieces, board) and
                not total_check([x, 6], c, loc_pieces, board) and
                any(piece_in_loc([x, 7], loc_pieces)) and
                board[x][7].moved == 0):
                list_moves2.append(['castle', 'right'])
            if (not any(piece_in_loc([x, 3], loc_pieces)) and
                not any(piece_in_loc([x, 2], loc_pieces)) and
                not any(piece_in_loc([x, 1], loc_pieces)) and
                not total_check([x, 4], c, loc_pieces, board) and
                not total_check([x, 3], c, loc_pieces, board) and
                not total_check([x, 2], c, loc_pieces, board) and
                not total_check([x, 1], c, loc_pieces, board) and
                any(piece_in_loc([x, 0], loc_pieces)) and
                board[x][0].moved == 0):
                list_moves2.append(['castle', 'left'])
        return list_moves2


class Queen(Piece):

    def __str__(self):
        return '\u265B' if self.color == 'w' else '\u2655'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        queenmoves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
        color = self.color
        for x, y in queenmoves:
            loop = True
            loc = self.loc
            while loop:
                new_loc = [loc[0] + x, loc[1] + y]
                list_moves, loop = valid_move(new_loc, loc_pieces, color, list_moves)
                loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, color, list_moves, board, loc_king)
        return list_moves


class Rook(Piece):

    def __str__(self):
        return '\u265C' if self.color == 'w' else '\u2656'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        rookmoves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        color = self.color
        for x, y in rookmoves:
            loop = True
            loc = self.loc
            while loop:
                new_loc = [loc[0] + x, loc[1] + y]
                list_moves, loop = valid_move(new_loc, loc_pieces, color, list_moves)
                loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, color, list_moves, board, loc_king)
        return list_moves


class Bishop(Piece):

    def __str__(self):
            return '\u265D' if self.color == 'w' else '\u2657'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        bishopmoves = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        color = self.color
        for x, y in bishopmoves:
            loop = True
            loc = self.loc
            while loop:
                new_loc = [loc[0] + x, loc[1] + y]
                list_moves, loop = valid_move(new_loc, loc_pieces, color, list_moves)
                loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, color, list_moves, board, loc_king)
        return list_moves


class Knight(Piece):

    def __str__(self):
        return '\u265E' if self.color == 'w' else '\u2658'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        knightmoves = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [2, -1], [1, -2], [2, 1], [1, 2]]
        loc = self.loc
        color = self.color
        for knightmove in knightmoves:
            new_loc = [loc[0] + knightmove[0], loc[1] + knightmove[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, color, list_moves)
        # remove moves that lead tot check
        list_moves = remove_moves_check(loc, color, list_moves, board, loc_king)
        return list_moves


class Pawn(Piece):

    def __str__(self):
        return '\u265F' if self.color == 'w' else '\u2659'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        color = self.color
        loc = self.loc
        moved = self.moved
        direction = -1 if color == 'w' else 1
        # forward moves
        new_loc = [loc[0] + direction, loc[1]]
        if not (0 > new_loc[0] or 7 < new_loc[0] or 0 > new_loc[1] or 7 < new_loc[1]):
            bool_list = piece_in_loc(new_loc, loc_pieces)
            if not any(bool_list):
                list_moves.append(new_loc)
                new_loc = [new_loc[0] + direction, new_loc[1]]
                if moved == 0 and not any(piece_in_loc(new_loc, loc_pieces)):
                    list_moves.append(new_loc)
        # takes moves
        locs = [[loc[0]+direction, loc[1]-1], [loc[0]+direction, loc[1]+1]]
        for locs_i in locs:
            if 0 > locs_i[0] or 7 < locs_i[0] or 0 > locs_i[1] or 7 < locs_i[1]:
                pass
            else:
                bool_list = piece_in_loc(locs_i, loc_pieces)
                if any(bool_list):
                    if color != array(loc_pieces)[array(bool_list)].tolist()[0][2]:
                        list_moves.append(locs_i)
        # en passant
        if (loc[0] == 3 and color == 'w') or (loc[0] == 4 and color == 'b'):
            for x, y in [[1, 'right'], [-1, 'left']]:
                if not(0 > loc[0] or 7 < loc[0] or 0 > loc[1] + x or 7 < loc[1] + x) and not board[loc[0]][loc[1] + x] == '':
                    if isinstance(board[loc[0]][loc[1] + x], Pawn) and move_count == board[loc[0]][loc[1] + x].moved:
                        list_moves.append(['en_passant', y])
        # remove moves that lead to check
        list_moves = remove_moves_check(loc, color, list_moves, board, loc_king)

        return list_moves
