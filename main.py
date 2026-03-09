import math


EMPTY = 0
HUMAN = 1
AI = 2

class Disc:
    # The disc object
    def __init__(self, owner: int):
        self.owner = owner

def create_board(n: int):
    #creates the board with the given size
    board = [[EMPTY] * n for _ in range(n)]
    return board


def print_board(board):
    n = len(board)
    line = "+" + "+".join(["---"] * n) + "+"
    print(line)
    for r in range(n):
        row = "|"
        for c in range(n):
            v = board[r][c]
            ch = " " if v == EMPTY else ("X" if v == HUMAN else "O")
            row += f" {ch} |"
        print(row)
        print(line)
    print(" " + " ".join(f" {i+1}" for i in range(n)))
    print()


    # checks for any column where top cell is empty
def valid_moves(board):
    n = len(board)
    moves = []
    for c in range(n):
        if board[0][c] == EMPTY:
            moves.append(c)
    return moves

    # places the piece in the lowest empty cell of the specified column, returns False if the move is invalid
def playerMove(board, col, player):
    n = len(board)
    if col < 0 or col >= n:
        print("Invalid column. Please choose a column between 1 and", n)
        return False
    if board[0][col] != EMPTY:
        print("Column is full. Please choose another column.")
        return False

    for r in range(n - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return True
    print("Column is full. Please choose another column.")
    return False

def undoMove(board, col):
    n = len(board)
    for r in range(n):
        if board[r][col] != EMPTY:
            board[r][col] = EMPTY
            return True
    return False

def check_win(board, player, M):
    n = len(board)
    for r in range(n):
        for c in range(n):
            if board[r][c] != player:
                continue
    #check horizontal
    if c + M - 1 < n:
        ok = True
        for k in range(M):
            if board[r][c + k] != player:
                ok = False
                break
            if ok:
                return True
    #check vertical
    if c + M - 1 < n:
        ok = True
        for k in range(M):
            if board[r + k][c] != player:
                ok = False
                break
            if ok:
                return True
    
    #check diagonal down-right
    if c + M - 1 < n:
        ok = True
        for k in range(M):
            if board[r + k][c + k] != player:
                ok = False
                break
            if ok: 
                return True
    #check diagonal down-left
    if c + M - 1 < n:
        ok = True
        for k in range(M):
            if board[r + k][c - k] != player:
                ok = False
                break
            if ok:
                return True
    
    return False
def gameOver(board, M):
    if check_win(board, HUMAN, M):
        return True
    if check_win(board, AI, M):
        return True
    if len(valid_moves(board)) == 0:
        return True
    return False

"User input, assigned to row and column"
m = int(input("What size matrix would you like?"))
rows, cols = m

"Creates the matrix"
matrix = [[0]* cols for _ in range(rows)]

def evaluation(board,M):
    if(check_win(board,AI,M)):
        return 1
    elif(check_win(board,HUMAN,M)):
        return -1
    else:
        return 0

"Algorithm to check the what move AI will do"
# If the full return the eval result
# If its the AI's turn, 
def minimax(alpha, beta, board, depth, maximizing, M):
    if depth==0 or gameOver(board, M):
        return  evaluation(board, M)
    
    if maximizing:
        max_value = -math.inf
        for col in valid_moves(board):
            playerMove(board, col, AI)
            value = minimax(alpha, beta, board, depth-1, False, M)
            undoMove(board, col)
            max_value = max(max_value, value)
            alpha = max(alpha, max_value)
            if alpha>=beta:
                break
        return max_value
    else:
        min_value = math.inf
        for col in valid_moves(board):
            playerMove(board, col, HUMAN)
            value = minimax(alpha, beta, board, depth-1, True, M)
            undoMove(board, col)
            min_value = min(min_value, value)
            beta = min(beta, min_value)
            if alpha>=beta:
                break
        return min_value

"Board to interact, col to place, player to place corrosponding piece"


def gameLoop(board):
    while True:
        "Get the user input as an int"
        col = int(input("Please"))
        playerMove(board,col,player=1)

        if gameOver(board):
            return "You've won!"
        col = minimax(alpha, beta, board, maximizing=true)
    pass