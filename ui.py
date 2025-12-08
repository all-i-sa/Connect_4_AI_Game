import pygame
from constants import ROWS, COLS, EMPTY, PLAYER, AI
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
RADIUS = SQUARESIZE // 2-5

# game window size
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE

# game colors
BG_COLOR = (235, 238, 243)
BOARD_COLOR = (66, 146, 250)
EMPTY_COLOR = (245, 245, 248)
PLAYER_COLOR = (237, 67, 62) # player (red color)
AI_COLOR = (253, 213, 71) # AI (yellow color)
TEXT_COLOR = (26, 104, 208)

def draw_board(screen, board):
    """Draw the Connect 4 board based on ROWS, COLS, and board state."""
    for row in range(ROWS):
        for col in range(COLS):
            # Board rectangle (background)
            pygame.draw.rect(
                screen,
                BOARD_COLOR,
                (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE),
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
                    (row + 1) * SQUARESIZE + SQUARESIZE // 2,
                ),
                RADIUS,
            )

def run_ui():
    """Pygame UI for Connect 4."""
    pygame.init()

    # create board
    board = create_board()
    game_over = False
    turn = PLAYER # player will start the game first
    hover_col = None # current col under the mouse
    status_text = ""

    # build window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4 Game")

    # font for status text
    font = pygame.font.SysFont("arial", 48, bold=True)

    running = True
    clock = pygame.time.Clock()

    # main event loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # hover column only for player move
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

            # handle mouse clicks by the player
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x = event.pos[0] # horizontal pos of mouse
                col = mouse_x // SQUARESIZE

                # ensure the player only moves when it is their turn
                if turn == PLAYER:
                    if 0 <= col < COLS and is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER)

                        # Check to see if it is a win
                        if check_winner(board, PLAYER):
                            print ("Player WINS!")
                            status_text = "Player WINS!"
                            game_over = True
                        else:
                            # check if draw
                            if len(get_valid_locations(board)) == 0:
                                print("Game is a DRAW!")
                                status_text = "Game is a DRAW!"
                                game_over = True
                            else:
                                screen.fill(BG_COLOR)
                                draw_board(screen, board)
                                pygame.display.flip()
                                # adding a pause so response to player is not immediate
                                pygame.time.wait(500)

                                # no one has won yet and game is not over so AI's turn
                                turn = AI
        # AI's turn
        if not game_over and turn == AI:
            valid_locations = get_valid_locations(board)
            if len(valid_locations) > 0:
                col = get_ai_move(board)

                if col is not None and is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI)

                    # check to see if AI won
                    if check_winner(board, AI):
                        print ("AI won!")
                        status_text = "AI WINS!"
                        game_over = True
                    else:
                        # check to see if draw
                        if len(get_valid_locations(board)) == 0:
                            print("Game ends in a draw!")
                            status_text = "Game is a DRAW!"
                            game_over = True
                        else:
                            # Game not over so player's turn again
                            turn = PLAYER

        # background color
        screen.fill(BG_COLOR)

        # draw hover piece at top for player
        if hover_col is not None and not game_over and turn == PLAYER:
            pygame.draw.circle(
                screen,
                PLAYER_COLOR,
                (
                    hover_col * SQUARESIZE + SQUARESIZE // 2,
                    SQUARESIZE // 2,
                ),
                RADIUS,
            )
        # draw board
        draw_board(screen, board)

        # game status message
        if status_text:
            text_surface = font.render(status_text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
            screen.blit(text_surface, text_rect)

        # update display
        pygame.display.flip()
        # max frames per second
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_ui()
