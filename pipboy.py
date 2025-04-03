import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 480  # Adjust for your HDMI LCD screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Pi Pip-Boy")

# Colors
GREEN = (57, 255, 20)  # Classic Pip-Boy green
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Screen types (tabs)
MAIN_SCREEN = 0
GPS_SCREEN = 1
WIKI_SCREEN = 2
RADIO_SCREEN = 3

# Start on the main screen
current_screen = MAIN_SCREEN

def draw_text(text, x, y, font_size=36, color=GREEN):
    font = pygame.font.Font(None, font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_panel(x, y, width, height, color=BLACK):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

def draw_borders():
    # Draw the central screen with borders
    draw_panel(10, 10, WIDTH - 20, HEIGHT - 20, (0, 0, 0))
    pygame.draw.rect(screen, GREEN, pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20), 5)

def draw_main_screen():
    draw_borders()
    draw_text("Raspberry Pi Pip-Boy", 250, 20, font_size=48)
    draw_text("System Status: Nominal", 250, 100, font_size=24)
    draw_text("Press [1] for GPS, [2] for Wiki, [3] for Radio", 250, HEIGHT - 60, font_size=24)

def draw_gps_screen():
    draw_borders()
    draw_text("GPS: Searching...", 50, 20, font_size=24)
    draw_text("Status: Not Locked", 50, 60, font_size=24)
    draw_text("Press [1] for Main Screen", 250, HEIGHT - 60, font_size=24)

def draw_wiki_screen():
    draw_borders()
    draw_text("Offline Wiki: Ready", 50, 20, font_size=24)
    draw_text("Press [1] for Main Screen", 250, HEIGHT - 60, font_size=24)

def draw_radio_screen():
    draw_borders()
    draw_text("Radio: Scanning...", 50, 20, font_size=24)
    draw_text("Press [1] for Main Screen", 250, HEIGHT - 60, font_size=24)

def main():
    global current_screen
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        # Draw the appropriate screen
        if current_screen == MAIN_SCREEN:
            draw_main_screen()
        elif current_screen == GPS_SCREEN:
            draw_gps_screen()
        elif current_screen == WIKI_SCREEN:
            draw_wiki_screen()
        elif current_screen == RADIO_SCREEN:
            draw_radio_screen()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Switch screens based on key press
                if event.key == pygame.K_1:  # Main screen
                    current_screen = MAIN_SCREEN
                elif event.key == pygame.K_2:  # GPS screen
                    current_screen = GPS_SCREEN
                elif event.key == pygame.K_3:  # Wiki screen
                    current_screen = WIKI_SCREEN
                elif event.key == pygame.K_4:  # Radio screen
                    current_screen = RADIO_SCREEN

        clock.tick(30)

if __name__ == "__main__":
    main()
