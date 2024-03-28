import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu Example")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)


# Function to display text on the screen
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Opening page
def opening_page():
    screen.fill(WHITE)
    draw_text("Welcome to Pygame!", WIDTH // 2, HEIGHT // 2 - 50, BLACK)
    draw_text("Press any key to start", WIDTH // 2, HEIGHT // 2 + 50, BLACK)
    pygame.display.flip()
    wait_for_key()


# Menu page
def menu_page():
    screen.fill(WHITE)
    draw_text("Game Menu", WIDTH // 2, HEIGHT // 4, BLACK)
    draw_text("1. Start Game", WIDTH // 2, HEIGHT // 2, BLACK)
    draw_text("2. Quit", WIDTH // 2, 3 * HEIGHT // 4, BLACK)
    pygame.display.flip()
    wait_for_key()


# Wait for a key press to proceed
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False






# Function to display input box
def draw_input_box(text, x, y, color):
    pygame.draw.rect(screen, WHITE, (x - 100, y - 20, 200, 40))
    pygame.draw.rect(screen, color, (x - 100, y - 20, 200, 40), 2)
    draw_text(text, x, y, color)

# Function to get user input
def get_user_input():
    input_text = ""
    input_active = True
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        draw_input_box(text, WIDTH // 2, HEIGHT // 2, color)
        pygame.display.flip()
        clock.tick(FPS)

    return text


# Menu page with input box
def menu_page():
    screen.fill(WHITE)
    draw_text("Game Menu", WIDTH // 2, HEIGHT // 4, BLACK)
    draw_text("1. Start Game", WIDTH // 2, HEIGHT // 2, BLACK)
    draw_text("2. Quit", WIDTH // 2, 3 * HEIGHT // 4, BLACK)
    input_text = get_user_input()
    print(f"User input: {input_text}")


# Game loop
def main():
    opening_page()

    while True:
        menu_page()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Starting Game...")
                    # Add your game logic here
                elif event.key == pygame.K_2:
                    print("Quitting Game...")
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)



if __name__ == "__main__":
    main()
