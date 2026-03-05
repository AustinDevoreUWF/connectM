class Disc:
    "The disc object"
    def __init__():
        pass

"Condition for the game to be over"
def gameOver():
    pass

"User input, assigned to row and column"
m = input("What size matrix would you like?")
rows, cols = m
"Creates the matrix"
matrix = [[0]* cols for _ in range(rows)]

"Algorithm to check the what move AI will do"
def minimax(alpha, beta, board, depth, maximizing):
    
    pass

"Board to interact, col to place, player to place corrosponding piece"
def playerMove(board, col, player):
    pass

def gameLoop(board):
    while True:
        "Get the user input as an int"
        col = int(input("Please"))
        playerMove(board,col,player=1)

        if gameOver(board):
            return "You've won!"
        col = minimax(alpha, beta, board, maximizing=true)
    pass