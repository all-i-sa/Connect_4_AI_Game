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

# size for the top UI area (buttons, status, hover)
HEADER_HEIGHT = 140  # taller header so nothing overlaps

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

BUTTON_BG = (245, 245, 248)
BUTTON_SELECTED_BG = (237, 67, 62)
BUTTON_TEXT_COLOR = (0, 0, 0)


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


def run_ui():
    """Pygame UI for Connect 4."""
    pygame.init()

    # create board
    board = create_board()
    game_over = False
    turn = PLAYER  # player starts
    hover_col = None
    status_text = ""

    current_depth = MEDIUM_DEPTH
    difficulty_name = "Medium"

    # AI thinking delay
    AI_DELAY_MS = 800  # pause
    ai_thinking = False
    ai_think_start = 0

    # window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4 Game")

    # fonts
    font = pygame.font.SysFont("arial", 36, bold=True)   # winner text
    small_font = pygame.font.SysFont("arial", 24)        # buttons/labels

    # difficulty button size
    button_width = 110
    button_height = 36
    button_y = 20

    easy_rect = pygame.Rect(10, button_y, button_width, button_height)
    medium_rect = pygame.Rect(20 + button_width, button_y, button_width, button_height)
    hard_rect = pygame.Rect(30 + 2 * button_width, button_y, button_width, button_height)

    # hover chip
    HOVER_Y = HEADER_HEIGHT - RADIUS - 10

    running = True
    clock = pygame.time.Clock()

    def draw_button(rect, label, selected):
        bg_color = BUTTON_SELECTED_BG if selected else BUTTON_BG
        border_color = TEXT_COLOR

        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

        label_surface = small_font.render(label, True, BUTTON_TEXT_COLOR)
        label_rect = label_surface.get_rect(center=rect.center)
        screen.blit(label_surface, label_rect)

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keyboard difficulty shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_depth = EASY_DEPTH
                    difficulty_name = "Easy"
                    print("Difficulty is set to easy (depth=", current_depth, ")")
                elif event.key == pygame.K_2:
                    current_depth = MEDIUM_DEPTH
                    difficulty_name = "Medium"
                    print("Difficulty is set to medium (depth=", current_depth, ")")
                elif event.key == pygame.K_3:
                    current_depth = HARD_DEPTH
                    difficulty_name = "Hard"
                    print("Difficulty is set to hard (depth=", current_depth, ")")

            # hover column only for player's turn
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

                # 1) check difficulty buttons in console
                if easy_rect.collidepoint(mouse_x, mouse_y):
                    current_depth = EASY_DEPTH
                    difficulty_name = "Easy"
                    print("Difficulty is set to easy (depth=", current_depth, ")")
                    continue
                elif medium_rect.collidepoint(mouse_x, mouse_y):
                    current_depth = MEDIUM_DEPTH
                    difficulty_name = "Medium"
                    print("Difficulty is set to medium (depth=", current_depth, ")")
                    continue
                elif hard_rect.collidepoint(mouse_x, mouse_y):
                    current_depth = HARD_DEPTH
                    difficulty_name = "Hard"
                    print("Difficulty is set to hard (depth=", current_depth, ")")
                    continue

                # 2) otherwise: treat board as click
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

        # ---- AI MOVE ------
        if not game_over and turn == AI:
            if ai_thinking:
                now = pygame.time.get_ticks()
                if now - ai_think_start >= AI_DELAY_MS:
                    ai_thinking = False

                    valid_locations = get_valid_locations(board)
                    if len(valid_locations) > 0:
                        col = get_ai_move(board, current_depth)

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
                # safety net if for some reason ai_thinking is False but it's AI's turn
                valid_locations = get_valid_locations(board)
                if len(valid_locations) > 0:
                    col = get_ai_move(board, current_depth)
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

# ------- visual builds ------

        # board
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

        # difficulty buttons
        draw_button(easy_rect, "Easy", difficulty_name.lower() == "easy")
        draw_button(medium_rect, "Medium", difficulty_name.lower() == "medium")
        draw_button(hard_rect, "Hard", difficulty_name.lower() == "hard")

        # winner or draw message
        if status_text:
            status_y = HEADER_HEIGHT // 1.5
            text_surface = font.render(status_text, True, WINNER_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, status_y))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_ui()
