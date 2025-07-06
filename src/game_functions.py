def check_winner(board, winner=0):
    for row in range(0,6):
        for col in range(0,7):
            #check for row win
            if col + 3 < 7:
                if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                    if board[row][col] is not None:
                        return board[row][col]
            #check for col win
            if row + 3 < 6:
                if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                    if board[row][col] is not None:
                        return board[row][col]
            #check for diagonal southeast win
            if row + 3 < 6 and col + 3 < 7:
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row+3][col+3]:
                    if board[row][col] is not None:
                        return board[row][col]
            #check for diagonal northeast win
            if row - 3 >= 0 and col + 3 < 7:
                if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                    if board[row][col] is not None:
                        return board[row][col] 
            #check for diagonal northwest win
            if row - 3 >= 0 and col - 3 >= 0:
                if board[row][col] == board[row-1][col-1] == board[row-2][col-2] == board[row-3][col-3]:
                    if board[row][col] is not None:
                        return board[row][col]
            #check for diagonal southwest win
            if row + 3 < 6 and col - 3 >= 0:
                if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3]:
                    if board[row][col] is not None:
                        return board[row][col]
    return None

def check_draw(board, board_is_full=False):
    for row in range(0,6):
        for col in range(0,7):
            if board[row][col] == None:
                board_is_full == True
    return board_is_full
    
def printBoard(board):
    for row in range (5,-1,-1):
        print(board[row])

def create_empty_board():
    return [[None for _ in range(7)] for _ in range(6)]

def apply_move(board, col, turn):
    placeRow = 5
    placed = False
    while placed == False:
        if placeRow <= 0:
            break
        if board[placeRow][col] != None:
            placeRow -= 1
        if board[placeRow][col] == None:
            if turn == 0:
                board[placeRow][col] = "1"
            elif turn == 1:
                board[placeRow][col] = "2"
            placed = True
    return placed