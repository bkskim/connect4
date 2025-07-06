import game_functions

board = game_functions.create_empty_board()

print("Welcome to Connect4!")

gameEnd = False
while gameEnd == False:
    #player 1 turn
    p1turn = int(input("Player 1 you are X's - choose a column to place your token. "))

    while p1turn < 1 or p1turn > 7:
        p1turn = int(input("Invalid column number. Enter a column number 1 through 7. "))

    placeRow = 0
    placed = False
    p1turn = p1turn - 1
    while placed == False:
        if board[placeRow][p1turn] != None:
            placeRow += 1
        if board[placeRow][p1turn] == None:
            board[placeRow][p1turn] = "X"
            placed = True

    #check if there's a winner
    if game_functions.check_winner(board) != None:
        gameEnd = True
        break

    game_functions.printBoard(board)

    #player 2 turn
    try:
        p2turn = int(input("Player 2 you are O's - choose a column to place your token. "))
    
    except:
        print("Invalid input. Enter a column number 1 through 7. ")

    while p2turn < 1 or p2turn > 7:
        p2turn = int(input("Invalid column number. Enter a column number 1 through 7. "))

    placeRow = 0
    placed = False
    p2turn = p2turn - 1
    while placed == False:
        if board[placeRow][p2turn] != None:
            placeRow += 1
        if board[placeRow][p2turn] == None:
            board[placeRow][p2turn] = "O"
            placed = True

    #check if there's a winner
    if game_functions.check_winner(board) != None:
        gameEnd = True
        break
    
    game_functions.printBoard(board)

winner = game_functions.check_winner(board)
if winner == "X":
    winner = "Player 1"
elif winner == "O":
    winner = "Player 2"
print(f"Game over! The winner is {winner}!")
print("The final board:")
game_functions.printBoard(board)