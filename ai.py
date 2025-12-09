import math
import random
import copy
from constants import ROWS, COLS, EMPTY, PLAYER, AI, DEPTH
from board import get_valid_locations, is_terminal_node, check_winner, get_next_open_row, drop_piece

def evaluate_window(window, piece):
    """Evaluate a window of 4 cells."""
    score = 0
    opponent = PLAYER if piece == AI else AI
    
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opponent_count = window.count(opponent)
    
    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2
    
    if opponent_count == 3 and empty_count == 1:
        score -= 4
    
    return score


def score_position(board, piece):
    """Evaluate the entire board position."""
    score = 0
    
    # Center column preference
    center_col = COLS // 2
    center_array = [board[row][center_col] for row in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning.
    
    Returns:
        (column, score) tuple
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board, AI):
                return (None, 100000000)
            elif check_winner(board, PLAYER):
                return (None, -100000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))
    
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, AI)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                best_col = col
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        return best_col, value
    
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, PLAYER)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                best_col = col
            
            beta = min(beta, value)
            if alpha >= beta:
                break
        
        return best_col, value


def get_ai_move(board, depth=None):
    """Get the AI's move using minimax.
    If depth is None, use the global DEPTH from constants (which is medium level)
    """
    if depth is None:
        depth = DEPTH

    col, _ = minimax(board, DEPTH, -math.inf, math.inf, True)
    return col

