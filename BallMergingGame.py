import pygame
import sys
from pygame.colordict import THECOLORS

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
PLAY_AREA_WIDTH = 600
PLAY_AREA_HEIGHT = 750

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Ball colors and radii
BALL_COLORS = ['blue4', 'brown1', 'brown3', 'burlywood1', 'yellow1', 'violetred4', 'tan1', 'red1', 'yellow2', 'yellowgreen', 'limegreen']
BALLS = [{"color": THECOLORS[color], "radius": (i + 1) * 0.5} for i, color in enumerate(BALL_COLORS)]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Merging Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Main game loop placeholder
def main():
    running = True
    score = 0
    high_score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw the play area
        pygame.draw.rect(
            screen, GRAY, 
            ((SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2, SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 50, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
        )

        # Draw the balls at the bottom
        ball_start_x = (SCREEN_WIDTH - sum(int(ball["radius"] * 10 * 2 + 2) for ball in BALLS)) // 2
        ball_y = SCREEN_HEIGHT - 25
        current_x = ball_start_x
        for ball in BALLS:
            radius_scaled = int(ball["radius"] * 10)
            pygame.draw.circle(screen, ball["color"], (current_x + radius_scaled, ball_y), radius_scaled)
            current_x += radius_scaled * 2 + 2  # Space by radius * 2 plus a buffer of 2

        # Draw the score and high score
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 20, 20))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()