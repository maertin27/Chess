from numpy import array
from chess_board import move_piece, location_pieces


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
    if outside_board(new_loc):
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
    if outside_board(new_loc):
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
        # up
    loop = True
    loc = loc_king
    while loop:
        new_loc = [loc[0] - 1, loc[1]]
        chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
        loc = new_loc
        # down
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0] + 1, loc[1]]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        # left
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0], loc[1] - 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        # right
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0], loc[1] + 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc

    # bishop and queen
    attackers = ['Bishop', 'Queen']
        # up left
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0] - 1, loc[1] - 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        # up right
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0] - 1, loc[1] + 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        # down left
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0] + 1, loc[1] - 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
        # down right
    if not chec:
        loop = True
        loc = loc_king
        while loop:
            new_loc = [loc[0] + 1, loc[1] + 1]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            loc = new_loc
    # knight
    attackers = ['Knight']
    if not chec:
        knightmoves = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [2, -1], [1, -2], [2, 1], [1, 2]]
        for move in knightmoves:
            new_loc = [loc_king[0] + move[0], loc_king[1] + move[1]]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break
    # pawn
    attackers = ['Pawn']
    if not chec:
        if color_king == 'w':
            direction = -1
        else:
            direction = 1
        locs = [[loc_king[0]+direction, loc_king[1]-1], [loc_king[0]+direction, loc_king[1]+1]]
        for loc in locs:
            chec, loop = check(loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break

    # king
    attackers = ['King']
    if not chec:
        kingmoves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, -1]]
        for kingmove in kingmoves:
            new_loc = [loc_king[0] + kingmove[0], loc_king[1] + kingmove[1]]
            chec, loop = check(new_loc, loc_pieces, attackers, board, color_king)
            if not chec:
                break

    return chec


def remove_moves_check(loc, color, list_moves, board, loc_pieces, loc_king):
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
    def __init__(self, loc, color):
        super().__init__(loc, color)
        self.castled = 'no'

    def __str__(self):
        if self.color == 'w':
            return '\u265A'
        else:
            return '\u2654'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        king_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        # generating possible moves
        for i in range(len(king_moves)):
            new_loc = [self.loc[0] + king_moves[i][0], self.loc[1] + king_moves[i][1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
        # removing moves that lead to checks
        list_moves2 = []
        for i in range(len(list_moves)):
            chec = total_check(list_moves[i], self.color, loc_pieces, board)
            if not chec:
                list_moves2.append(list_moves[i])
        # castling
        if self.moved == 0:
            if self.color == 'w':
                # right castling
                if (not any(piece_in_loc([7, 5], loc_pieces)) and
                    not any(piece_in_loc([7, 6], loc_pieces)) and
                    not total_check([7, 4], 'w', loc_pieces, board) and
                    not total_check([7, 5], 'w', loc_pieces, board) and
                    not total_check([7, 6], 'w', loc_pieces, board) and
                    any(piece_in_loc([7, 7], loc_pieces)) and
                    board[7][7].moved == 0):
                    list_moves2.append(['castle', 'right'])
                if (not any(piece_in_loc([7, 3], loc_pieces)) and
                    not any(piece_in_loc([7, 2], loc_pieces)) and
                    not any(piece_in_loc([7, 1], loc_pieces)) and
                    not total_check([7, 4], 'w', loc_pieces, board) and
                    not total_check([7, 3], 'w', loc_pieces, board) and
                    not total_check([7, 2], 'w', loc_pieces, board) and
                    not total_check([7, 1], 'w', loc_pieces, board) and
                    any(piece_in_loc([7, 0], loc_pieces)) and
                    board[7][0].moved == 0):
                    list_moves2.append(['castle', 'left'])
            else:
                if (not any(piece_in_loc([0, 5], loc_pieces)) and
                    not any(piece_in_loc([0, 6], loc_pieces)) and
                    not total_check([0, 4], 'b', loc_pieces, board) and
                    not total_check([0, 5], 'b', loc_pieces, board) and
                    not total_check([0, 6], 'b', loc_pieces, board) and
                    any(piece_in_loc([0, 7], loc_pieces)) and
                    board[0][7].moved == 0):
                    list_moves2.append(['castle', 'right'])
                if (not any(piece_in_loc([0, 3], loc_pieces)) and
                    not any(piece_in_loc([0, 2], loc_pieces)) and
                    not any(piece_in_loc([0, 1], loc_pieces)) and
                    not total_check([0, 4], 'b', loc_pieces, board) and
                    not total_check([0, 3], 'b', loc_pieces, board) and
                    not total_check([0, 2], 'b', loc_pieces, board) and
                    not total_check([0, 1], 'b', loc_pieces, board) and
                    any(piece_in_loc([0, 0], loc_pieces)) and
                    board[0][0].moved == 0):
                    list_moves2.append(['castle', 'left'])

        return list_moves2


class Queen(Piece):
    def __str__(self):
        if self.color == 'w':
            return '\u265B'
        else:
            return '\u2655'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        # up
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # down
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0], loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0], loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # up left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # up right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # down left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # down right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, self.color, list_moves, board, loc_pieces, loc_king)
        return list_moves


class Rook(Piece):

    def __str__(self):
        if self.color == 'w':
            return '\u265C'
        else:
            return '\u2656'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        # up
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc

        # down
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0], loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0], loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, self.color, list_moves, board, loc_pieces, loc_king)
        return list_moves


class Bishop(Piece):
    def __str__(self):
        if self.color == 'w':
            return '\u265D'
        else:
            return '\u2657'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        # up left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # up right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] - 1, loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # down left
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1] - 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # down right
        loop = True
        loc = self.loc
        while loop:
            new_loc = [loc[0] + 1, loc[1] + 1]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
            loc = new_loc
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, self.color, list_moves, board, loc_pieces, loc_king)
        return list_moves


class Knight(Piece):
    def __str__(self):
        if self.color == 'w':
            return '\u265E'
        else:
            return '\u2658'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        knightmoves = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [2, -1], [1, -2], [2, 1], [1, 2]]
        loc = self.loc
        for i in range(len(knightmoves)):
            new_loc = [loc[0] + knightmoves[i][0], loc[1] + knightmoves[i][1]]
            list_moves, loop = valid_move(new_loc, loc_pieces, self.color, list_moves)
        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, self.color, list_moves, board, loc_pieces, loc_king)
        return list_moves


class Pawn(Piece):
    def __str__(self):
        if self.color == 'w':
            return '\u265F'
        else:
            return '\u2659'

    def __repr__(self):
        return str(self)

    def moves(self, board, loc_pieces, loc_king, move_count):
        list_moves = []
        if self.color == 'w':
            direction = -1
        else:
            direction = 1
        # forward moves
        moves = 0
        loc = self.loc
        while moves < 2:
            new_loc = [loc[0] + direction, loc[1]]

            if outside_board(new_loc):
                moves = 2
            else:
                bool_list = piece_in_loc(new_loc, loc_pieces)
                if any(bool_list):
                    moves = 2
                else:
                    list_moves.append(new_loc)
                if self.moved == 0:
                    moves += 1
                else:
                    moves = 2
            loc = new_loc
        # takes moves
        loc = self.loc
        locs = [[loc[0]+direction, loc[1]-1], [loc[0]+direction, loc[1]+1]]
        for i in range(len(locs)):
            if outside_board(locs[i]):
                pass
            else:
                bool_list = piece_in_loc(locs[i], loc_pieces)
                if any(bool_list):
                    if self.color != array(loc_pieces)[array(bool_list)].tolist()[0][2]:
                        list_moves.append(locs[i])
        # en passant
        if loc[0] == 3 and self.color == 'w':  # TODO
            if not outside_board([loc[0], loc[1] + 1]) and not board[loc[0]][loc[1] + 1] == ' ':
                if 'Pawn' == type(board[loc[0]][loc[1] + 1]).__name__ and move_count == board[loc[0]][loc[1] + 1].moved:
                    list_moves.append(['en_passant', 'right'])
            if not outside_board([loc[0], loc[1] - 1]) and not board[loc[0]][loc[1] - 1] == ' ':
                if 'Pawn' == type(board[loc[0]][loc[1] - 1]).__name__ and move_count == board[loc[0]][loc[1] - 1].moved:
                    list_moves.append(['en_passant', 'left'])
        elif loc[0] == 4 and self.color == 'b':
            if not outside_board([loc[0], loc[1] + 1]) and not board[loc[0]][loc[1] + 1] == ' ':
                if 'Pawn' == type(board[loc[0]][loc[1] + 1]).__name__ and move_count == board[loc[0]][loc[1] + 1].moved:
                    list_moves.append(['en_passant', 'right'])
            if not outside_board([loc[0], loc[1] - 1]) and not board[loc[0]][loc[1] - 1] == ' ':
                if 'Pawn' == type(board[loc[0]][loc[1] - 1]).__name__ and move_count == board[loc[0]][loc[1] - 1].moved:
                    list_moves.append(['en_passant', 'left'])

        # remove moves that lead tot check
        list_moves = remove_moves_check(self.loc, self.color, list_moves, board, loc_pieces, loc_king)

        return list_moves
