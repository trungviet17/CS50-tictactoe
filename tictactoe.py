import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    - X is first move, O is last move
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count <= o_count:
        return X
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Invalid action')

    new_board = copy.deepcopy(board)
    curr_player = player(board)
    new_board[action[0]][action[1]] = curr_player
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return board[2][0]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    curr_player = player(board)
    if curr_player == 'X':
        best_val = -math.inf
        best_act = None
        for action in actions(board):
            new_val = min_val(result(board, action))
            if new_val > best_val:
                best_val = new_val
                best_act = action
    else:
        best_val = math.inf
        best_act = None
        for action in actions(board):
            new_val = max_val(result(board, action))
            if new_val < best_val:
                best_val = new_val
                best_act = action

    return best_act

def min_val(board):
    if terminal(board):
        return utility(board)

    x = math.inf
    for action in actions(board):
        x = min(x, max_val(result(board, action)))
    return x

def max_val(board):
    if terminal(board):
        return utility(board)

    x = -math.inf
    for action in actions(board):
        x = max(x, min_val(result(board, action)))
    return x
