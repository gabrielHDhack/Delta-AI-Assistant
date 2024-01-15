import tkinter as tk
import random

def check_win(board, player):
    # Check if the player has won by examining rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check if the player has won by examining columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check if the player has won by examining diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    # Check if the game is a draw by ensuring all cells are filled
    return all(cell != "" for row in board for cell in row)

def computer_move(board):
    # Check if the computer can win in the next move
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                if check_win(board, "O"):
                    return (row, col)
                board[row][col] = ""

    # Check if the player can win in the next move and block them
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "X"
                if check_win(board, "X"):
                    return (row, col)
                board[row][col] = ""

    # If no immediate winning moves, make a random move
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ""]
    return random.choice(empty_cells)

def restart_game(buttons, result_label, board):
    # Clear the buttons and result label
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="")
    result_label.config(text="")
    # Reset the content of the provided 'board' list
    for i in range(3):
        for j in range(3):
            board[i][j] = ""

def player_move(board, buttons, result_label, game_over, row, col):
    # Handle the player's move if the cell is empty and the game is not over
    if board[row][col] == "" and not game_over:
        # Update the board and button text
        board[row][col] = "X"
        buttons[row][col].config(text="X")
        # Check if the player has won
        if check_win(board, "X"):
            result_label.config(text="You won!")
            game_over = True
        # Check if the game is a draw
        elif check_draw(board):
            result_label.config(text="It's a draw!")
            game_over = True
        else:
            # If the game is not over, let the computer make a move
            row, col = computer_move(board)
            board[row][col] = "O"
            buttons[row][col].config(text="O")
            # Check if the computer has won
            if check_win(board, "O"):
                result_label.config(text="Delta AI won!")
                game_over = True
            # Check if the game is a draw
            elif check_draw(board):
                result_label.config(text="It's a draw!")
                game_over = True

def create_board_buttons(root, buttons, player_move_func):
    # Create buttons for the Tic-Tac-Toe grid
    for i in range(3):
        row_buttons = []
        for j in range(3):
            button = tk.Button(root, text="", width=10, height=3, command=lambda row=i, col=j: player_move_func(row, col))
            button.grid(row=i, column=j)
            row_buttons.append(button)
        buttons.append(row_buttons)

def create_restart_button(root, restart_func):
    # Create a button to restart the game
    restart_button = tk.Button(root, text="Restart", command=restart_func)
    restart_button.grid(row=3, columnspan=3)

def create_result_label(root):
    # Create a label to display the game result
    result_label = tk.Label(root, text="", font=("Helvetica", 16))
    result_label.grid(row=4, columnspan=3)
    return result_label

def main():
    # Initialize the Tkinter window
    root = tk.Tk()
    # Initialize the game state
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False

    buttons = []
    result_label = create_result_label(root)
    # Create the game board buttons and restart button
    create_board_buttons(root, buttons, lambda row, col: player_move(board, buttons, result_label, game_over, row, col))
    create_restart_button(root, lambda: restart_game(buttons, result_label, board))

    # Enter the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
