import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari Breakout")

# Colors (Atari 2600 palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (227, 30, 36)
ORANGE = (255, 149, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 216, 0)
PURPLE = (180, 60, 220)

# Game elements
paddle_width = 80
paddle_height = 12
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50

ball_size = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-4, -3, 3, 4])
ball_dy = -4

# Brick setup - Atari style (2 rows per color)
brick_width = 80
brick_height = 20
bricks_per_row = WIDTH // brick_width
rows = 8

# Create bricks list with Atari colors
bricks = []
brick_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, RED, ORANGE]

for row in range(rows):
    for col in range(bricks_per_row):
        brick_x = col * brick_width
        brick_y = row * brick_height + 50
        bricks.append({
            "rect": pygame.Rect(brick_x, brick_y, brick_width, brick_height),
            "color": brick_colors[row],
            "hit": False
        })

# Game state
score = 0
lives = 3
game_over = False
game_started = False  # Game doesn't start until player clicks

# Font for score display (Atari-style font)
font = pygame.font.SysFont('Courier', 24, bold=True)
title_font = pygame.font.SysFont('Courier', 48, bold=True)

# Sound effects
try:
    paddle_sound = pygame.mixer.Sound(pygame.sndarray.array(
        [random.randint(-32768, 32767) for _ in range(2205)]))  # Beep sound
    brick_sound = pygame.mixer.Sound(pygame.sndarray.array(
        [int(32767 * math.sin(2 * math.pi * 880 * i / 44100)) for i in range(2205)]))  # Higher pitch
    wall_sound = pygame.mixer.Sound(pygame.sndarray.array(
        [int(32767 * math.sin(2 * math.pi * 440 * i / 44100)) for i in range(1102)]))  # Lower pitch
except:
    # Fallback if sound doesn't work
    paddle_sound = brick_sound = wall_sound = None

def draw_objects():
    # Draw paddle (Atari-style rectangle)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height), 2)
    
    # Draw ball (Atari-style square)
    pygame.draw.rect(screen, WHITE, (int(ball_x - ball_size//2), int(ball_y - ball_size//2), ball_size, ball_size))
    
    # Draw bricks with Atari-style borders
    for brick in bricks:
        if not brick["hit"]:
            pygame.draw.rect(screen, brick["color"], brick["rect"])
            pygame.draw.rect(screen, WHITE, brick["rect"], 2)
    
    # Draw score and lives (Atari-style display)
    score_text = font.render(f"SCORE: {score:04d}", True, WHITE)
    screen.blit(score_text, (20, 15))
    
    lives_text = font.render(f"LIVES: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 15))
    
    # Draw game over or start message
    if game_over:
        game_over_text = title_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
    
    elif not game_started:
        start_text = title_font.render("ATARI BREAKOUT", True, YELLOW)
        instruction_text = font.render("Click to Start", True, WHITE)
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, lives, score, game_over, game_started, bricks, paddle_x
    
    # Reset ball position
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-4, -3, 3, 4])
    ball_dy = -4
    
    # Reset paddle position
    paddle_x = WIDTH // 2 - paddle_width // 2
    
    # Reset game state
    lives = 3
    score = 0
    game_over = False
    game_started = True
    
    # Reset bricks
    bricks = []
    for row in range(rows):
        for col in range(bricks_per_row):
            brick_x = col * brick_width
            brick_y = row * brick_height + 50
            bricks.append({
                "rect": pygame.Rect(brick_x, brick_y, brick_width, brick_height),
                "color": brick_colors[row],
                "hit": False
            })

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Mouse click to start game
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            game_started = True
        
        # Restart game
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()
    
    # Move paddle with mouse
    if game_started and not game_over:
        paddle_x, _ = pygame.mouse.get_pos()
        paddle_x = max(0, min(paddle_x, WIDTH - paddle_width))  # Keep paddle on screen
        
        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collision with walls
        if ball_x <= ball_size//2:
            ball_dx = -ball_dx
            ball_x = ball_size//2
            if wall_sound: wall_sound.play()
        elif ball_x >= WIDTH - ball_size//2:
            ball_dx = -ball_dx
            ball_x = WIDTH - ball_size//2
            if wall_sound: wall_sound.play()
        
        if ball_y <= ball_size//2:
            ball_dy = -ball_dy
            ball_y = ball_size//2
            if wall_sound: wall_sound.play()
        
        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        ball_rect = pygame.Rect(ball_x - ball_size//2, ball_y - ball_size//2, 
                               ball_size, ball_size)
        
        if ball_rect.colliderect(paddle_rect) and ball_dy > 0:
            # Calculate bounce angle based on where the ball hit the paddle
            relative_x = (ball_x - (paddle_x + paddle_width/2)) / (paddle_width/2)
            angle = relative_x * 0.8  # Limit the angle
            
            ball_dx = 5 * math.sin(angle)
            ball_dy = -5 * math.cos(angle)
            if paddle_sound: paddle_sound.play()
        
        # Ball falls below paddle
        if ball_y >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset ball position
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = random.choice([-4, -3, 3, 4])
                ball_dy = -4
        
        # Brick collision
        for brick in bricks:
            if not brick["hit"] and brick["rect"].colliderect(ball_rect):
                # Determine which side of the brick was hit
                if abs(ball_rect.bottom - brick["rect"].top) < 10 and ball_dy > 0:
                    ball_dy = -ball_dy  # Hit from bottom
                elif abs(ball_rect.top - brick["rect"].bottom) < 10 and ball_dy < 0:
                    ball_dy = -ball_dy  # Hit from top
                elif abs(ball_rect.right - brick["rect"].left) < 10 and ball_dx > 0:
                    ball_dx = -ball_dx  # Hit from left
                elif abs(ball_rect.left - brick["rect"].right) < 10 and ball_dx < 0:
                    ball_dx = -ball_dx  # Hit from right
                
                brick["hit"] = True
                score += 10
                if brick_sound: brick_sound.play()
                break  # Only break one brick per frame
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw scanlines for authentic Atari look
    for i in range(0, HEIGHT, 4):
        pygame.draw.line(screen, (20, 20, 30), (0, i), (WIDTH, i), 1)
    
    draw_objects()
    
    pygame.display.flip()
    clock.tick(60)
