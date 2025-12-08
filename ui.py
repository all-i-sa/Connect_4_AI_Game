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
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)      # could be PLAYER
YELLOW = (255, 255, 0) # could be AI

def draw_board(screen, board):
    """Draw the Connect 4 board based on ROWS, COLS, and board state."""
    for row in range(ROWS):
        for col in range(COLS):
            # Board rectangle (background)
            pygame.draw.rect(
                screen,
                BLUE,
                (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )

            cell_value = board[row][col]

            if cell_value == EMPTY:
                piece_color = WHITE
            elif cell_value == PLAYER:
                piece_color = RED
            elif cell_value == AI:
                piece_color = YELLOW
            else:
                piece_color = WHITE  # fallback

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

    # build window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4 - UI Test")

    running = True
    clock = pygame.time.Clock()

    # main event loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                            game_over = True
                        else:
                            # check if draw
                            if len(get_valid_locations(board)) == 0:
                                print("Game is a DRAW!")
                                game_over = True
                            else:
                                screen.fill(BLACK)
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
                        game_over = True
                    else:
                        # check to see if draw
                        if len(get_valid_locations(board)) == 0:
                            print("Game ends in a draw!")
                            game_over = True
                        else:
                            # Game not over so player's turn again
                            turn = PLAYER

        # background color
        screen.fill(BLACK)
        # draw board
        draw_board(screen, board)

        # update display
        pygame.display.flip()

        # max frames per second
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_ui()
