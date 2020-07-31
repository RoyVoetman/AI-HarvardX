"""
Tic Tac Toe Player
"""

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
    """
    Xcount = 0
    Ocount = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                Xcount = Xcount + 1
            elif board[i][j] == O:
                Ocount = Ocount + 1

    if Xcount == 0 and Ocount == 0:
        return X # X is starting player when game begins
    
    return O if Xcount > Ocount else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == EMPTY):
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] >= 3 or action[1] >= 3:
        raise InvalidMoveError("Out of range cords")

    if board[action[0]][action[1]] != EMPTY:
        raise InvalidMoveError("Invalid tile")

    board = copy.deepcopy(board)
    board[action[0]][action[1]] = player(board)

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizontal lines
    for i in range(len(board)):
        if board[i][0] == EMPTY: continue

        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]

    # Check vertical lines
    for j in range(len(board[0])):
        if board[0][j] == EMPTY: continue

        if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            return board[0][j]

    # Check diagonal lines
    if board[1][1] != EMPTY:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[1][1]

        if board[2][0] == board[1][1] and board[1][1] == board[0][2]:
            return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                return False
    
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    _winner = winner(board)

    if _winner == None:
        return 0

    return 1 if _winner == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    isMaximizing = True if player(board) == X else False
    
    bestMove = traverseTree(board, isMaximizing)

    return (bestMove.row, bestMove.column)

def traverseTree(board, isMaximizing):
    """
    Build minimax tree recursively and return the optimal
    """
    if terminal(board):
        return Move(utility(board))

    bestRow = -1
    bestColumn = -1

    # Building the tree
    bestScore = -math.inf if isMaximizing else math.inf

    possibleActions = actions(board)

    for action in possibleActions:
        move = traverseTree(result(board, action), not isMaximizing)

        if (isMaximizing and move.score > bestScore) or (not isMaximizing and move.score < bestScore):
            bestScore = move.score
            bestRow = action[0]
            bestColumn = action[1]

    return Move(bestScore, bestRow, bestColumn)

def prettyBoard(board):
    """
    Debug function to print board in terminal
    """
    for i in range(len(board)):
        print("| ", end='')
        for j in range(len(board[i])):
            char = board[i][j] if board[i][j] != None else " "
            print(char + " | ", end = '')
        print("")

class Move():
    def __init__(self, score, row=None, column=None):
        self.score = score
        self.row = row
        self.column = column

class InvalidMoveError(RuntimeError):
   def __init__(self, arg):
      self.args = arg