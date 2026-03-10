import math
import sys

EMPTY = 0
HUMAN = 1
AI = 2

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
    print(" " + "  ".join(f" {i+1}" for i in range(n)))
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

            # horizontal
            if c + M <= n:
                if all(board[r][c + k] == player for k in range(M)):
                    return True

            # vertical
            if r + M <= n:
                if all(board[r + k][c] == player for k in range(M)):
                    return True

            # diagonal down-right
            if r + M <= n and c + M <= n:
                if all(board[r + k][c + k] == player for k in range(M)):
                    return True

            # diagonal down-left
            if r + M <= n and c - M + 1 >= 0:
                if all(board[r + k][c - k] == player for k in range(M)):
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

# Formatted gameloop with AI
def gameLoop(board, M, depth=4, human_first=True):
    human_turn=human_first
    print_board(board)

    while not gameOver(board, M):
        if human_turn:
            while True:
                try:
                    col = int(input(f"Your move (1-{len(board)}): "))-1
                    if playerMove(board,col,HUMAN):
                        break
                except ValueError:
                    print("Please enter a valid column")
            print_board(board)
        else:
            print("ConnectM-Bot is thinking about its next move...")
            best_col, best_val = None, -math.inf
            for c in valid_moves(board):
                playerMove(board,c,AI)
                val = minimax(-math.inf, math.inf, board, depth-1,False,M)
                undoMove(board, c)
                if val>best_val:
                    best_val, best_col = val,c
            playerMove(board,best_col,AI)
            print(f"AI chose column {best_col+1}")
            print_board(board)
        human_turn = not human_turn

    if check_win(board, HUMAN, M):
        print("You win!")
    elif check_win(board, AI, M):
        print("AI wins!")
    else:
        print("It's a draw!")

if len(sys.argv) != 4:
    print("Usage: python connectM.py N M H")
    print("  N = board size (3-10)")
    print("  M = discs to connect (2-N)")
    print("  H = who goes first: 1 = human, 0 = computer")
    sys.exit(1)

try:
    N = int(sys.argv[1])
    M = int(sys.argv[2])
    H = int(sys.argv[3])
except ValueError:
    print("Error: N, M, and H must all be integers.")
    sys.exit(1)

if not (3 <= N <= 10):
    print("Error: N must be between 3 and 10.")
    sys.exit(1)
if not (2 <= M <= N):
    print("Error: M must be between 2 and N.")
    sys.exit(1)
if H not in (0, 1):
    print("Error: H must be 0 (computer first) or 1 (human first).")
    sys.exit(1)

board = create_board(N)
print(f"\nConnect {M} — {N}x{N} board")
print(f"You are X, AI is O. {'You go first.' if H == 1 else 'Computer goes first.'}\n")

gameLoop(board, M, depth=4, human_first=(H == 1))