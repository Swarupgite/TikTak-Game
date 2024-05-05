import pygame
import sys

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
PUCK_SIZE = 15
PUCK_SPEED = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Game objects
player1_color = (0, 128, 255)  # Blue color for player 1 paddle
player2_color = (255, 128, 0)  # Orange color for player 2 paddle
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
puck = pygame.Rect(WIDTH // 2 - PUCK_SIZE // 2, HEIGHT // 2 - PUCK_SIZE // 2, PUCK_SIZE, PUCK_SIZE)
puck_speed_x = PUCK_SPEED
puck_speed_y = PUCK_SPEED

# Scores
score_player1 = 0
score_player2 = 0

# Font
font = pygame.font.Font(None, 36)

# Game state
GAME_RUNNING = 'running'
GAME_PAUSED = 'paused'
GAME_OVER = 'game_over'
game_state = GAME_RUNNING

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == GAME_OVER:
            if restart_button.collidepoint(event.pos):
                game_state = GAME_RUNNING
                score_player1 = 0
                score_player2 = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == GAME_RUNNING:
                    game_state = GAME_PAUSED
                elif game_state == GAME_PAUSED:
                    game_state = GAME_RUNNING

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= PADDLE_SPEED
    if keys[pygame.K_d] and player1.right < WIDTH // 2:
        player1.x += PADDLE_SPEED
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED
    if keys[pygame.K_LEFT] and player2.left > WIDTH // 2:
        player2.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and player2.right < WIDTH:
        player2.x += PADDLE_SPEED

    # Puck movement
    if game_state == GAME_RUNNING:
        puck.x += puck_speed_x
        puck.y += puck_speed_y

    # Puck collisions
    if puck.top <= 0 or puck.bottom >= HEIGHT:
        puck_speed_y *= -1
    if puck.colliderect(player1) or puck.colliderect(player2):
        puck_speed_x *= -1

    # Scoring
    if puck.left <= 0:
        # Player 2 scores
        score_player2 += 1
        if score_player2 >= 5:
            game_state = GAME_OVER
        else:
            puck_speed_x = PUCK_SPEED
            puck_speed_y = PUCK_SPEED
            puck.center = (WIDTH // 2, HEIGHT // 2)
    elif puck.right >= WIDTH:
        # Player 1 scores
        score_player1 += 1
        if score_player1 >= 5:
            game_state = GAME_OVER
        else:
            puck_speed_x = -PUCK_SPEED
            puck_speed_y = -PUCK_SPEED
            puck.center = (WIDTH // 2, HEIGHT // 2)

    # Drawing
    screen.fill(BLACK)
    
    # Draw player 1 paddle with color and shading
    pygame.draw.rect(screen, player1_color, player1)
    pygame.draw.rect(screen, WHITE, player1, 3)  # Add a white border for a 3D effect
    
    # Draw player 2 paddle with color and shading
    pygame.draw.rect(screen, player2_color, player2)
    pygame.draw.rect(screen, WHITE, player2, 3)  # Add a white border for a 3D effect
    
    pygame.draw.ellipse(screen, RED, puck)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Display scores
    text_player1 = font.render(f"Player A: {score_player1}", True, WHITE)
    text_player2 = font.render(f"Player B: {score_player2}", True, WHITE)
    screen.blit(text_player1, (20, 20))
    screen.blit(text_player2, (WIDTH - 180, 20))

    # Display winner
    if game_state == GAME_OVER:
        winner_text = font.render("Player A wins!" if score_player1 >= 5 else "Player B wins!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2))
        restart_button = pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50))
        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - 40, HEIGHT // 2 + 60))

    # Display pause message
    if game_state == GAME_PAUSED:
        pause_text = font.render("Paused", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
