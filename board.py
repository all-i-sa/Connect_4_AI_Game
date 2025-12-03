from constants import ROWS, COLS, EMPTY, PLAYER, AI

def create_board():
    """Create an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Simple text display of the board."""
    print("\n  1 2 3 4 5 6 7")
    print("  " + "-" * 15)
    for row in board:
        print("  " + " ".join(str(cell) for cell in row))
    print()

def is_valid_location(board, col):
    return board[0][col] == EMPTY


def get_valid_locations(board):
    """Get all columns that can accept a piece."""
    return [col for col in range(COLS) if is_valid_location(board, col)]


def get_next_open_row(board, col):
    """Find the lowest empty row in a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board, row, col, piece):
    """Place a piece on the board."""
    board[row][col] = piece


def check_winner(board, piece):
    """Check if the given piece has won."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    
    # Diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    
    # Diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    
    return False


def is_terminal_node(board):
    """Check if the game is over."""
    return (check_winner(board, PLAYER) or 
            check_winner(board, AI) or 
            len(get_valid_locations(board)) == 0)
