import pieces as p
import copy



dictionary = {
    # making a dictionary used in function coord
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0,
}


def make_board():
    # Makes a list of the initial board with the corresponding objects as pieces and empty strings as empty spaces
    # Also starts a counter for the amount of played moves
    board = [[p.Rook([0, 0], 'b'), p.Knight([0, 1], 'b'), p.Bishop([0, 2], 'b'), p.Queen([0, 3], 'b'), p.King([0, 4], 'b'), p.Bishop([0, 5], 'b'), p.Knight([0, 6], 'b'), p.Rook([0, 7], 'b')],
             [p.Pawn([1, 0], 'b'), p.Pawn([1, 1], 'b'), p.Pawn([1, 2], 'b'), p.Pawn([1, 3], 'b'), p.Pawn([1, 4], 'b'), p.Pawn([1, 5], 'b'), p.Pawn([1, 6], 'b'), p.Pawn([1, 7], 'b')],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [p.Pawn([6, 0], 'w'), p.Pawn([6, 1], 'w'), p.Pawn([6, 2], 'w'), p.Pawn([6, 3], 'w'), p.Pawn([6, 4], 'w'), p.Pawn([6, 5], 'w'), p.Pawn([6, 6], 'w'), p.Pawn([6, 7], 'w')],
             [p.Rook([7, 0], 'w'), p.Knight([7, 1], 'w'), p.Bishop([7, 2], 'w'), p.Queen([7, 3], 'w'), p.King([7, 4], 'w'), p.Bishop([7, 5], 'w'), p.Knight([7, 6], 'w'), p.Rook([7, 7], 'w')]]
    move_count = 0
    return board, move_count


def move_piece(board, fro, to, move_count):
    # moves the pieces around the board
    # has as inputs the board, fro(from), to and move_count
    # fro is has the coordinates of the piece.
    # to has the coordinates of the place to move to or has the strings 'castle' or 'en_passant'

    board2 = copy.deepcopy(board)
    move_count += 1
    if to[0] == 'castle':
        board2 = castling(board2, to[1], board2[fro[0]][fro[1]].color, move_count)
    elif to[0] == 'en_passant':
        board2 = en_passant(board2, fro[1], to[1], board2[fro[0]][fro[1]].color, move_count)
    elif (board2[fro[0]][fro[1]].color == 'w' and fro[0] == 1) \
            or (board2[fro[0]][fro[1]].color == 'b' and fro[0] == 7) \
            and isinstance(board2[fro[0]][fro[1]], p.Pawn):
        board2[to[0]][to[1]] = p.Queen([to[0], to[1]], board2[fro[0]][fro[1]].color)
        board2[to[0]][to[1]].moved = move_count
        board2[fro[0]][fro[1]] = ' '
    else:
        board2[to[0]][to[1]] = board2[fro[0]][fro[1]]
        board2[to[0]][to[1]].loc = [to[0], to[1]]
        board2[to[0]][to[1]].moved = move_count
        board2[fro[0]][fro[1]] = ' '

    return board2, move_count


def print_board(board):
    # prints the board row per row and adds borders containing coordinate names
    numbers = [8, 7, 6, 5, 4, 3, 2, 1]
    for row in range(8):
        print('')
        print(numbers[row], end=' ')
        for column in range(8):
            print(board[row][column], end=' ')
    print('')

    for i in [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        print(i, end=' ')
    print('')
    print('-'*19)


def coord(place):
    # transforms chess coordinates into coordinares usable to move pieces through the list
    return [dictionary[place[1]], dictionary[place[0]]]


def castling(board, direction, color, move_count):
    # function to castle depending on inputs: direction(l/r) and color (w/b)
    errormsg = 'Invalid input: enter the board, the direction of castling(left/right) and the color of castling(w/b)'

    if color == 'w':
        x = 7
    elif color == 'b':
        x = 0
    else:
        print(errormsg)

    if direction == 'right':
        board[x][4] = ' '
        board[x][5] = p.Rook([x, 5], 'w')
        board[x][6] = p.King([x, 6], 'w')
        board[x][7] = ' '
        board[x][5].moved = move_count
        board[x][6].moved = move_count
    elif direction == 'left':
        board[x][0] = ' '
        board[x][2] = p.Rook([x, 2], 'w')
        board[x][3] = p.King([x, 3], 'w')
        board[x][4] = ' '
        board[x][2].moved = move_count
        board[x][3].moved = move_count
    else:
        print(errormsg)

    return board


def en_passant(board, column, direction, color, move_count):
    # function to en_passant depending on inputs: direction(l/r) and color (w/b)
    errormsg = 'Invalid input: enter the board,file(a/b/c..), the direction of en passant(left/right) ' \
               'and the color of en passant(w/b)'
    x = column
    if color == 'w':
        if direction == 'left':
            board[3][x] = ' '
            board[3][x - 1] = ' '
            board[2][x - 1] = p.Pawn([2, x - 1], 'w')
            board[2][x - 1].moved = move_count

        elif direction == 'right':
            board[3][x] = ' '
            board[3][x + 1] = ' '
            board[2][x + 1] = p.Pawn([2, x + 1], 'w')
            board[2][x + 1].moved = move_count
        else:
            print(errormsg)
    elif color == 'b':
        if direction == 'left':
            board[4][x] = ' '
            board[4][x - 1] = ' '
            board[5][x - 1] = p.Pawn([5, x - 1], 'b')
            board[5][x - 1].moved = move_count
        elif direction == 'right':
            board[4][x] = ' '
            board[4][x + 1] = ' '
            board[5][x + 1] = p.Pawn([5, x + 1], 'b')
            board[5][x + 1].moved = move_count
        else:
            print(errormsg)
    else:
        print(errormsg)

    return board


def location_pieces(board):
    # loops through whole board to find coordinates of every piece
    loc_list = []
    for row in range(8):
        for column in range(8):
            if type(board[row][column]).__name__ != 'str':
                loc_list.append([row, column, board[row][column].color])
    return loc_list


def location_king(board, loc_pieces, color):
    # loops through list loc_pieces to find the king of one color
    i = 0
    loc_king = []
    length = len(loc_pieces)
    while not loc_king:
        if type(board[loc_pieces[i][0]][loc_pieces[i][1]]).__name__ == 'King' and loc_pieces[i][2] == color:
            loc_king = loc_pieces[i]
        i += 1
        if i == length:
            break
    return loc_king


def generate_all_moves(board, loc_pieces, color, loc_king, move_count):
    # makes a list of all possible moves dor all pieces of one color by using implemented .moves
    # syntax all_moves: [[loc_piece,[move,move,move,...]],[loc_piece,[move,move,move,...]],...]
    all_moves = []
    for loc_piece in loc_pieces:
        loc0 = loc_piece[0]
        loc1 = loc_piece[1]
        if loc_piece[2] == color:
            x = [[loc0, loc1], board[loc0][loc1].moves(board, loc_pieces, loc_king, move_count)]
            if x[1]:
                all_moves.append(x)
    return all_moves


def score_function(board, loc_pieces):
    # calculates score for board assigning classic amount of points according to the pieces.
    # positive score is in favor of white, negative in favor for black.
    score_black = 0
    score_white = 0
    for loc_piece in loc_pieces:
        while True:
            typ = type(board[loc_piece[0]][loc_piece[1]]).__name__
            if 'Pawn' == typ:
                if loc_piece[2] == 'w':
                    score_white += 1
                else:
                    score_black += 1
                break
            if 'Knight' == typ:
                if loc_piece[2] == 'w':
                    score_white += 3
                else:
                    score_black += 3
                break
            if 'Bishop' == typ:
                if loc_piece[2] == 'w':
                    score_white += 3
                else:
                    score_black += 3
                break
            if 'Rook' == typ:
                if loc_piece[2] == 'w':
                    score_white += 5
                else:
                    score_black += 5
                break
            if 'Queen' == typ:
                if loc_piece[2] == 'w':
                    score_white += 9
                else:
                    score_black += 9
                break
            if 'King' == typ:
                if loc_piece[2] == 'w':
                    score_white += 100
                else:
                    score_black += 100
                break
    score = score_white - score_black
    return score




