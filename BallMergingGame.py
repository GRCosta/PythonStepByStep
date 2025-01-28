import pygame
import sys
import random
from pygame.colordict import THECOLORS

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
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

def initialize_game():
    """Initialize the game state."""
    # Select a random ball to drop
    selected_ball = random.choice(BALLS)
    ball = {
        "color": selected_ball["color"],
        "radius": int(selected_ball["radius"] * 10),
        "x": SCREEN_WIDTH // 2,
        "y": SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 200 - int(selected_ball["radius"] * 10)
    }
    return ball

# Main game loop placeholder
def main():
    running = True
    score = 0
    high_score = 0

    # Initialize game state
    ball = initialize_game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set the ball's x position to the mouse's x position
                ball["x"] = event.pos[0]

        # Clear the screen
        screen.fill(WHITE)

        # Draw the play area
        pygame.draw.rect(
            screen, GRAY, 
            ((SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2, SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 200, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
        )

        # Update the ball's position (simulate falling)
        if ball["y"] < SCREEN_HEIGHT - 200 - ball["radius"]:
            ball["y"] += 5  # Falling speed

        # Draw the ball
        pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball["radius"])

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
