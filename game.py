from constants import COLS, PLAYER, AI
from board import create_board, print_board, is_valid_location, get_valid_locations, get_next_open_row, drop_piece,check_winner
from ai import get_ai_move




def get_player_move(board):
    while True:
        try:
            col = int(input("Choose column (1-7): ")) - 1
            if 0 <= col < COLS and is_valid_location(board, col):
                return col
            print("Invalid move. Try again.")
        except ValueError:
            print("Enter a number 1-7.")


def play_game():
    """Main game loop for testing."""
    board = create_board()
    game_over = False
    turn = PLAYER
    
    print_board(board)
    
    while not game_over:
        if turn == PLAYER:
            col = get_player_move(board)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER)
            
            if check_winner(board, PLAYER):
                print_board(board)
                print("You win!")
                game_over = True
            else:
                turn = AI
                
        else:
            col = get_ai_move(board)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI)
            
            if check_winner(board, AI):
                print_board(board)
                print("AI wins!")
                game_over = True
            else:
                turn = PLAYER
        
        if not game_over:
            print_board(board)
            if len(get_valid_locations(board)) == 0:
                print("Draw!")
                game_over = True