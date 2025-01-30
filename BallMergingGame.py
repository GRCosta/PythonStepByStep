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
BALL_COLORS = [
    'blue4', 'brown1', 'brown3', 'burlywood1', 'yellow1',
    'violetred4', 'tan1', 'red1', 'yellow2', 'yellowgreen', 'limegreen'
]
BALLS = [
    {"color": THECOLORS[color], "radius": (i + 1) * 0.5} for i, color in enumerate(BALL_COLORS)
]

# Limit balls to first 5 radii for dropping
DROPPABLE_BALLS = BALLS[:5]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Merging Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# List to store all dropped balls
previous_balls = []

def initialize_game():
    """Initialize the game state."""
    # Select a random ball to drop
    selected_ball = random.choice(DROPPABLE_BALLS)
    ball = {
        "color": selected_ball["color"],
        "radius": int(selected_ball["radius"] * 10),
        "x": SCREEN_WIDTH // 2,
        "y": SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 200 - int(selected_ball["radius"] * 10),
        "falling": False  # Indicates whether the ball is falling
    }
    return ball

def reset_ball(ball):
    """Reset the ball to prepare for the next drop."""
    selected_ball = random.choice(DROPPABLE_BALLS)
    ball.update({
        "color": selected_ball["color"],
        "radius": int(selected_ball["radius"] * 10),
        "x": SCREEN_WIDTH // 2,
        "y": SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 200 - int(selected_ball["radius"] * 10),
        "falling": False
    })

def handle_events(ball):
    """Handle player input and system events."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not ball["falling"]:
        ball["x"] -= 5  # Continuous movement left
        # Restrict ball to stay inside the left boundary of the play area
        min_x = (SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2 + ball["radius"]
        if ball["x"] < min_x:
            ball["x"] = min_x
    if keys[pygame.K_RIGHT] and not ball["falling"]:
        ball["x"] += 5  # Continuous movement right
        # Restrict ball to stay inside the right boundary of the play area
        max_x = (SCREEN_WIDTH + PLAY_AREA_WIDTH) // 2 - ball["radius"]
        if ball["x"] > max_x:
            ball["x"] = max_x
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Signal to exit the game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball["falling"]:
                ball["falling"] = True  # Start the ball falling
        elif event.type == pygame.MOUSEBUTTONDOWN and not ball["falling"]:
            ball["falling"] = True  # Start the ball falling
    return True

def draw_balls_row():
    """Draw the row of balls at the bottom for reference."""
    x_start = 20
    y_position = SCREEN_HEIGHT - 100
    for ball in BALLS:
        radius = int(ball["radius"] * 10)
        pygame.draw.circle(screen, ball["color"], (x_start + radius + 2, y_position), radius)
        x_start += 2 * radius + 10

def draw_dropped_balls():
    """Draw all balls that have been dropped into the play area."""
    for dropped_ball in previous_balls:
        pygame.draw.circle(screen, dropped_ball["color"], (dropped_ball["x"], dropped_ball["y"]), dropped_ball["radius"])

def update_game_state():
    """Update the game state by checking for merges and updating positions."""
    merged = []
    to_remove = set()  # Store indexes of merged balls

    for i in range(len(previous_balls)):
        for j in range(i + 1, len(previous_balls)):  # Avoid duplicate checks
            if i in to_remove or j in to_remove:
                continue  # Skip if the ball is already merged

            ball1 = previous_balls[i]
            ball2 = previous_balls[j]

            if ball1 is not None and ball2 is not None and check_ball_merge(ball1, ball2):
                # Merge logic: create a new ball with the next radius
                new_radius = ball1["radius"] + 5
                if new_radius <= 50:  # Limit the maximum radius
                    new_ball = {
                        "color": THECOLORS[BALL_COLORS[(new_radius // 5) - 1]],
                        "radius": new_radius,
                        "x": (ball1["x"] + ball2["x"]) // 2,
                        "y": (ball1["y"] + ball2["y"]) // 2
                    }
                    merged.append(new_ball)

                # Mark the balls as processed
                to_remove.add(i)
                to_remove.add(j)

    # Remove merged balls safely
    global merged_balls
    merged_balls = [ball for idx, ball in enumerate(previous_balls) if idx not in to_remove]
    merged_balls.extend(merged)
    
def check_ball_merge(ball1, ball2):
    """Check if two balls should merge based on their proximity and radius."""
    distance = ((ball1["x"] - ball2["x"]) ** 2 + (ball1["y"] - ball2["y"]) ** 2) ** 0.5
    return distance < (ball1["radius"] + ball2["radius"] + 2) and ball1["radius"] == ball2["radius"]

def main():
    running = True
    score = 0
    high_score = 0

    # Initialize game state
    ball = initialize_game()

    while running:
        # Handle events
        running = handle_events(ball)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the play area
        pygame.draw.rect(
            screen, GRAY, 
            ((SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2, SCREEN_HEIGHT - PLAY_AREA_HEIGHT - 200, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
        )

        # Draw the row of balls
        draw_balls_row()

        # Draw dropped balls
        draw_dropped_balls()

        # Update the ball's position (simulate falling)
        if ball["falling"]:
            if ball["y"] < SCREEN_HEIGHT - 200 - ball["radius"]:
                ball["y"] += 5  # Falling speed
            else:
                previous_balls.append(ball.copy())  # Save the ball's final position
                reset_ball(ball)  # Reset the ball for the next drop

        # Update game state
        update_game_state()

        # Draw the current falling ball
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
