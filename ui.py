import time
import pygame
from constants import ROWS, COLS, EMPTY, PLAYER, AI, EASY_DEPTH, MEDIUM_DEPTH, HARD_DEPTH
from board import (
    create_board,
    is_valid_location,
    get_next_open_row,
    drop_piece,
    check_winner,
    get_valid_locations,
)
from ai import get_ai_move

# visual settings
SQUARESIZE = 80
RADIUS = SQUARESIZE // 2 - 5

# size for the top UI area (reduced since no buttons)
HEADER_HEIGHT = 80

# game window size
WIDTH = COLS * SQUARESIZE
HEIGHT = HEADER_HEIGHT + ROWS * SQUARESIZE

# game colors
BG_COLOR = (235, 238, 243)
BOARD_COLOR = (66, 146, 250)
EMPTY_COLOR = (245, 245, 248)
PLAYER_COLOR = (237, 67, 62)  # player (red)
AI_COLOR = (253, 213, 71)      # AI (yellow)
TEXT_COLOR = (26, 104, 208)
WINNER_TEXT_COLOR = (0, 0, 0)

# Return to menu button colors
MENU_BUTTON_BG = (237, 67, 62)  # Red
MENU_BUTTON_HOVER = (200, 50, 50)  # Darker red
MENU_BUTTON_TEXT = (255, 255, 255)  # White


def draw_board(screen, board):
    """Draw the Connect 4 board below the header."""
    for row in range(ROWS):
        for col in range(COLS):
            # Board rectangle (background)
            pygame.draw.rect(
                screen,
                BOARD_COLOR,
                (
                    col * SQUARESIZE,
                    HEADER_HEIGHT + row * SQUARESIZE,
                    SQUARESIZE,
                    SQUARESIZE,
                ),
            )

            cell_value = board[row][col]

            if cell_value == EMPTY:
                piece_color = EMPTY_COLOR
            elif cell_value == PLAYER:
                piece_color = PLAYER_COLOR
            elif cell_value == AI:
                piece_color = AI_COLOR
            else:
                piece_color = EMPTY_COLOR  # fallback

            pygame.draw.circle(
                screen,
                piece_color,
                (
                    col * SQUARESIZE + SQUARESIZE // 2,
                    HEADER_HEIGHT + row * SQUARESIZE + SQUARESIZE // 2,
                ),
                RADIUS,
            )


def run_ui(initial_depth=None, initial_difficulty_name=None):
    """Pygame UI for Connect 4 with continuous gameplay loop."""
    
    # Set initial difficulty from menu or default to Medium
    if initial_depth is not None and initial_difficulty_name is not None:
        current_depth = initial_depth
        difficulty_name = initial_difficulty_name
    else:
        current_depth = MEDIUM_DEPTH
        difficulty_name = "Medium"

    pygame.init()
    
    # window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Connect 4 Game - {difficulty_name} Mode")

    # fonts
    font = pygame.font.SysFont("arial", 36, bold=True)   # winner text
    small_font = pygame.font.SysFont("arial", 20)        # instruction text

    # AI thinking delay (UI pause)
    AI_DELAY_MS = 800

    # move/compute times for each AI difficulty level
    move_times = {
        "Easy": [],
        "Medium": [],
        "Hard": [],
    }

    clock = pygame.time.Clock()
    running = True
    return_to_menu = False  # Flag to break continuous loop

    # Return to menu button
    menu_button_width = 120
    menu_button_height = 35
    menu_button_x = WIDTH - menu_button_width - 10
    menu_button_y = 10
    menu_button_rect = pygame.Rect(menu_button_x, menu_button_y, menu_button_width, menu_button_height)

    # Main continuous game loop
    while running and not return_to_menu:
        # Reset game state for new round
        board = create_board()
        game_over = False
        turn = PLAYER  # player starts
        hover_col = None
        status_text = ""
        ai_thinking = False
        ai_think_start = 0
        stats_printed = False
        
        # hover area
        HOVER_Y = HEADER_HEIGHT - RADIUS - 10

        # Individual game loop
        while running and not game_over:
            # ----- EVENT HANDLING -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                # keyboard shortcuts for difficulty level
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        current_depth = EASY_DEPTH
                        difficulty_name = "Easy"
                        pygame.display.set_caption(f"Connect 4 Game - {difficulty_name} Mode")
                        print("Difficulty is set to easy (depth=", current_depth, ")")
                    elif event.key == pygame.K_2:
                        current_depth = MEDIUM_DEPTH
                        difficulty_name = "Medium"
                        pygame.display.set_caption(f"Connect 4 Game - {difficulty_name} Mode")
                        print("Difficulty is set to medium (depth=", current_depth, ")")
                    elif event.key == pygame.K_3:
                        current_depth = HARD_DEPTH
                        difficulty_name = "Hard"
                        pygame.display.set_caption(f"Connect 4 Game - {difficulty_name} Mode")
                        print("Difficulty is set to hard (depth=", current_depth, ")")

                # hover column for players turn
                if event.type == pygame.MOUSEMOTION:
                    if not game_over and turn == PLAYER:
                        mouse_x = event.pos[0]
                        col = mouse_x // SQUARESIZE
                        if 0 <= col < COLS:
                            hover_col = col
                        else:
                            hover_col = None
                    else:
                        hover_col = None

                # mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Check if return to menu button is clicked
                    if menu_button_rect.collidepoint(mouse_x, mouse_y):
                        print("Returning to main menu...")
                        return_to_menu = True
                        game_over = True  # End current game immediately
                        break

                    if not game_over:
                        col = mouse_x // SQUARESIZE

                        if turn == PLAYER:
                            if 0 <= col < COLS and is_valid_location(board, col):
                                row = get_next_open_row(board, col)
                                drop_piece(board, row, col, PLAYER)

                                if check_winner(board, PLAYER):
                                    print("Player WINS!")
                                    status_text = "Player WINS!"
                                    game_over = True
                                else:
                                    if len(get_valid_locations(board)) == 0:
                                        print("Game is a DRAW!")
                                        status_text = "Game is a DRAW!"
                                        game_over = True
                                    else:
                                        # switch to AI, start "thinking" timer
                                        turn = AI
                                        ai_thinking = True
                                        ai_think_start = pygame.time.get_ticks()

            # ----- AI MOVE -----
            if not game_over and turn == AI:
                if ai_thinking:
                    now = pygame.time.get_ticks()
                    if now - ai_think_start >= AI_DELAY_MS:
                        ai_thinking = False

                        valid_locations = get_valid_locations(board)
                        if len(valid_locations) > 0:
                            # measure compute time of minimax
                            start = time.perf_counter()
                            col = get_ai_move(board, current_depth)
                            end = time.perf_counter()
                            elapsed = end - start

                            if difficulty_name in move_times:
                                move_times[difficulty_name].append(elapsed)
                            print(f"[{difficulty_name}] AI move took {elapsed:.4f} seconds")

                            if col is not None and is_valid_location(board, col):
                                row = get_next_open_row(board, col)
                                drop_piece(board, row, col, AI)

                                if check_winner(board, AI):
                                    print("AI won!")
                                    status_text = "AI WINS!"
                                    game_over = True
                                else:
                                    if len(get_valid_locations(board)) == 0:
                                        print("Game ends in a draw!")
                                        status_text = "Game is a DRAW!"
                                        game_over = True
                                    else:
                                        turn = PLAYER
                else:
                    # safety net if somehow ai_thinking is False but it's AI's turn
                    valid_locations = get_valid_locations(board)
                    if len(valid_locations) > 0:
                        start = time.perf_counter()
                        col = get_ai_move(board, current_depth)
                        end = time.perf_counter()
                        elapsed = end - start

                        if difficulty_name in move_times:
                            move_times[difficulty_name].append(elapsed)
                        print(f"[{difficulty_name}] AI move took {elapsed:.4f} seconds")

                        if col is not None and is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, AI)
                            if check_winner(board, AI):
                                status_text = "AI WINS!"
                                game_over = True
                            elif len(get_valid_locations(board)) == 0:
                                status_text = "Game is a DRAW!"
                                game_over = True
                            else:
                                turn = PLAYER

            # ----- RENDERING -----
            screen.fill(BG_COLOR)

            # hover piece
            if hover_col is not None and not game_over and turn == PLAYER:
                pygame.draw.circle(
                    screen,
                    PLAYER_COLOR,
                    (
                        hover_col * SQUARESIZE + SQUARESIZE // 2,
                        HOVER_Y,
                    ),
                    RADIUS,
                )

            # board
            draw_board(screen, board)

            # Display difficulty mode at top left (away from menu button)
            mode_text = small_font.render(f"Difficulty: {difficulty_name}", True, TEXT_COLOR)
            screen.blit(mode_text, (10, 20))

            # winner/draw message
            if status_text:
                status_y = HEADER_HEIGHT // 2 + 10
                text_surface = font.render(status_text, True, WINNER_TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, status_y))
                screen.blit(text_surface, text_rect)

            # print summary of AI stats when game ends
            if game_over and not stats_printed:
                print("\n=== AI Move/Computation Stats ===")
                for diff, times in move_times.items():
                    if times:
                        avg = sum(times) / len(times)
                        print(f"{diff}: {len(times)} moves, average {avg:.4f} seconds per move")
                stats_printed = True

            # Draw return to menu button LAST so it's on top
            mouse_pos = pygame.mouse.get_pos()
            menu_button_hovered = menu_button_rect.collidepoint(mouse_pos)
            button_color = MENU_BUTTON_HOVER if menu_button_hovered else MENU_BUTTON_BG
            pygame.draw.rect(screen, button_color, menu_button_rect, border_radius=8)
            menu_text = small_font.render("Menu", True, MENU_BUTTON_TEXT)
            menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
            screen.blit(menu_text, menu_text_rect)

            pygame.display.flip()
            clock.tick(60)

        # Game over - wait for a moment then start new game
        if running and game_over and not return_to_menu:
            # Show result for 3 seconds
            pygame.time.wait(3000)
            print("\n--- Starting new game ---\n")

    # Clear event queue before returning to menu
    pygame.event.clear()
    print("Exiting run_ui, returning to main menu...")
    # Don't quit pygame here - let the caller handle it


if __name__ == "__main__":
    run_ui()
    pygame.quit()