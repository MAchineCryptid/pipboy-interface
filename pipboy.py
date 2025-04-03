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

# Initialize frame counter for blinking text
frame_counter = 0

def draw_text(text, x, y, font_size=36, color=GREEN):
    font = pygame.font.Font(None, font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_glow_text(text, x, y, font_size=36, glow_color=GREEN):
    # Draw glow effect by rendering text multiple times in different positions
    for offset in range(3, 0, -1):  # Different offsets for the glow
        draw_text(text, x + offset, y + offset, font_size, color=glow_color)
    draw_text(text, x, y, font_size, color=GREEN)

def draw_scanlines():
    line_height = 2  # Space between each scanline
    for y in range(0, HEIGHT, line_height * 2):  # Skip every other line
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), line_height)

def fade_in():
    for alpha in range(0, 255, 5):  # Gradually increase alpha
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def fade_out():
    for alpha in range(255, 0, -5):  # Gradually decrease alpha
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def draw_button(x, y, width, height, text, hover=False):
    if hover:
        pygame.draw.rect(screen, GREEN, pygame.Rect(x - 5, y - 5, width + 10, height + 10), 3)  # Glow on hover
    pygame.draw.rect(screen, GREEN, pygame.Rect(x, y, width, height))
    draw_text(text, x + 10, y + 10, font_size=24)

def is_mouse_hover(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return x < mouse_x < x + width and y < mouse_y < y + height

def draw_blinking_text(text, x, y, font_size=36, color=GREEN, blink_speed=500):
    global frame_counter
    frame_counter += 1
    
    # Blink logic: Show text every "blink_speed" frames
    if frame_counter % blink_speed < blink_speed // 2:
        draw_text(text, x, y, font_size, color)

def draw_main_screen():
    draw_scanlines()
    fade_in()
    draw_glow_text("Raspberry Pi Pip-Boy", 250, 20, font_size=48)
    
    # Blinking text for system status
    draw_blinking_text("System Status: Nominal", 250, 100, font_size=24)
    
    draw_text("Press [1] for GPS, [2] for Wiki, [3] for Radio", 250, HEIGHT - 60, font_size=24)

    # Draw buttons
    mouse_hover = is_mouse_hover(50, HEIGHT - 100, 200, 40)
    draw_button(50, HEIGHT - 100, 200, 40, "Start GPS", hover=mouse_hover)

def draw_gps_screen():
    draw_scanlines()
    draw_glow_text("GPS: Searching...", 50, 20, font_size=24)
    draw_text("Status: Not Locked", 50, 60, font_size=24)
    draw_text("Press [1] for Main Screen", 250, HEIGHT - 60, font_size=24)

def draw_wiki_screen():
    draw_scanlines()
    draw_glow_text("Offline Wiki: Ready", 50, 20, font_size=24)
    draw_text("Press [1] for Main Screen", 250, HEIGHT - 60, font_size=24)

def draw_radio_screen():
    draw_scanlines()
    draw_glow_text("Radio: Scanning...", 50, 20, font_size=24)
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
                    fade_out()
                    current_screen = MAIN_SCREEN
                    fade_in()
                elif event.key == pygame.K_2:  # GPS screen
                    fade_out()
                    current_screen = GPS_SCREEN
                    fade_in()
                elif event.key == pygame.K_3:  # Wiki screen
                    fade_out()
                    current_screen = WIKI_SCREEN
                    fade_in()
                elif event.key == pygame.K_4:  # Radio screen
                    fade_out()
                    current_screen = RADIO_SCREEN
                    fade_in()

        clock.tick(30)

if __name__ == "__main__":
    main()
