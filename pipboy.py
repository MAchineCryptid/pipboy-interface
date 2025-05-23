import pygame
import psutil
import os
import time

# Initialize Pygame
pygame.init()

# Define colors for the yellow monochrome theme
YELLOW = (255, 255, 0)  # Pip-Boy Amber
DARK_YELLOW = (174, 149, 64)  # Muted amber for inactive tabs
BLACK = (0, 0, 0)

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pip-Boy Interface")

# Set up basic font (default Pygame font)
font = pygame.font.SysFont("monospace", 36)  # Default Pygame monospace font
small_font = pygame.font.SysFont("monospace", 24)  # Smaller monospace font

# Function to render text on the screen
def draw_text(text, x, y, font_size=36, color=YELLOW):
    font = pygame.font.SysFont("monospace", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to apply a yellow color filter to the background image
def apply_yellow_filter(image):
    yellow_image = image.copy()
    width, height = yellow_image.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = yellow_image.get_at((x, y))
            yellow_image.set_at((x, y), (min(r + 50, 174), min(g + 50, 149), min(b + 20, 64), a))  # Apply filter
    return yellow_image

# Function to draw the STATUS screen
def draw_status_screen():
    screen.fill(BLACK)  # Fill the screen with black background

    # Background image
    background_image = pygame.image.load("background.png")
    background_image = apply_yellow_filter(background_image)
    screen.blit(background_image, (0, 0))

    # Draw the "G.E.C.K." text on the Status screen
    draw_text("G.E.C.K.", 280, 60, font_size=48, color=YELLOW)

    # Draw CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    draw_text(f"CPU Usage: {cpu_usage}%", 50, 120, font_size=36, color=YELLOW)

    # Handle Battery Status or Power Draw
    battery = psutil.sensors_battery()
    if battery is not None:
        battery_percent = battery.percent
        draw_text(f"Battery: {battery_percent}%", 50, 180, font_size=36, color=YELLOW)
    else:
        # If no battery, display power plugged status
        power_plugged = psutil.sensors_battery() and psutil.sensors_battery().power_plugged
        if power_plugged:
            draw_text(f"Power Draw: Active", 50, 180, font_size=36, color=YELLOW)
        else:
            draw_text(f"Power Draw: Inactive", 50, 180, font_size=36, color=YELLOW)

    # Draw Storage Space Available
    total, used, free = psutil.disk_usage('/')
    storage_available = free // (2**30)  # Convert to GB
    draw_text(f"Storage Available: {storage_available} GB", 50, 240, font_size=36, color=YELLOW)

    # Draw the small text at the bottom for Date and Time
    current_time = time.strftime("%m-%d-%Y %H:%M:%S")
    draw_text(current_time, 50, SCREEN_HEIGHT - 30, font_size=18, color=DARK_YELLOW)

    pygame.display.update()

# Function to handle the drawing of other screens (WIKI, GPS, RADIO)
def draw_other_screens(screen_name):
    screen.fill(BLACK)  # Fill with black for other screens
    draw_text(screen_name, 50, 50, font_size=48, color=YELLOW)
    pygame.display.update()

# Main function to handle screen transitions
def main():
    clock = pygame.time.Clock()
    running = True
    current_screen = "STATUS"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handling tab navigation with TAB and SHIFT+TAB
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if current_screen == "STATUS":
                        current_screen = "WIKI"
                    elif current_screen == "WIKI":
                        current_screen = "GPS"
                    elif current_screen == "GPS":
                        current_screen = "RADIO"
                    else:
                        current_screen = "STATUS"
                elif event.key == pygame.K_SHIFT:
                    if current_screen == "STATUS":
                        current_screen = "RADIO"
                    elif current_screen == "WIKI":
                        current_screen = "STATUS"
                    elif current_screen == "GPS":
                        current_screen = "WIKI"
                    else:
                        current_screen = "GPS"

        # Draw the current screen
        if current_screen == "STATUS":
            draw_status_screen()
        else:
            draw_other_screens(current_screen)

        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
