import pygame
from ui import run_ui
from constants import EASY_DEPTH, MEDIUM_DEPTH, HARD_DEPTH

# Initialize Pygame
pygame.init()

# Screen dimensions (match ui.py game window)
WIDTH, HEIGHT = 560, 560

# Define blue background color
BLUE_BG = (0, 0, 255)

# Set up fonts (adjusted for 560x560 window)
title_font = pygame.font.SysFont('comicsansms', 60)
font = pygame.font.SysFont('comicsansms', 36)      

# Define button properties (adjusted for 560x560 window)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

button_width, button_height = 300, 60 
border_radius = 15                   

# Function to draw text on the screen
def draw_text(text, font, color, x, y, screen):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Function to draw buttons
def draw_button(text, x, y, width, height, hovered, border_radius, screen):
    color = RED if hovered else YELLOW
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    draw_text(text, font, BLACK, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2, screen)

# Main game loop
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    
    running = True
    while running:
        # Fill the background with blue
        screen.fill(BLUE_BG)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Button positions and sizes (center the buttons horizontally)
        button_positions = [
            ((WIDTH - button_width) // 2, 150, "EASY"),
            ((WIDTH - button_width) // 2, 230, "MEDIUM"),
            ((WIDTH - button_width) // 2, 310, "HARD"),
            ((WIDTH - button_width) // 2, 390, "Exit")
        ]

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button is clicked
                for (x, y, text) in button_positions:
                    if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                        if text == "EASY":
                            print("Starting Easy mode...")
                            run_ui(EASY_DEPTH, "Easy")
                            # When run_ui returns, recreate the screen for menu
                            print("Returned from Easy mode, reloading menu...")
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                            pygame.display.set_caption("Connect 4")
                        elif text == "MEDIUM":
                            print("Starting Medium mode...")
                            run_ui(MEDIUM_DEPTH, "Medium")
                            # When run_ui returns, recreate the screen for menu
                            print("Returned from Medium mode, reloading menu...")
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                            pygame.display.set_caption("Connect 4")
                        elif text == "HARD":
                            print("Starting Hard mode...")
                            run_ui(HARD_DEPTH, "Hard")
                            # When run_ui returns, recreate the screen for menu
                            print("Returned from Hard mode, reloading menu...")
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                            pygame.display.set_caption("Connect 4")
                        elif text == "Exit":
                            running = False
                            pygame.quit()
                            return

        # Draw title at the top of the screen
        draw_text("Connect 4", title_font, (255, 255, 255), (WIDTH - title_font.size("Connect 4")[0]) // 2, 40, screen)

        # Draw buttons with rounded corners
        for (x, y, text) in button_positions:
            hovered = x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height
            draw_button(text, x, y, button_width, button_height, hovered, border_radius, screen)

        # Update display
        pygame.display.flip()

# Main function to start the menu
if __name__ == "__main__":
    main_menu()