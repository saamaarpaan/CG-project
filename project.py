import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - CG Project")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE, GRAY = (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200)

# Fonts
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 40)

# Paddle and Ball
paddle_width, paddle_height = 100, 15
paddle_speed = 7
ball_radius = 10
ball_speed_x, ball_speed_y = 4, -4

# Bricks
brick_rows, brick_cols = 5, 10
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

def create_bricks():
    bricks.clear()
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick = pygame.Rect(col * brick_width, row * brick_height + 50, brick_width - 2, brick_height - 2)
            bricks.append(brick)

def draw_menu():
    screen.fill(BLACK)
    title = big_font.render("Brick Breaker", True, BLUE)
    start = font.render("1. Start Game", True, WHITE)
    instructions = font.render("2. Instructions", True, WHITE)
    quit_game = font.render("3. Quit", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 200))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 250))
    screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, 300))
    pygame.display.flip()

def draw_instructions():
    screen.fill(BLACK)
    lines = [
        "INSTRUCTIONS:",
        "- Move paddle: Arrow keys (← / →)",
        "- Break all bricks to win.",
        "- Ball should not fall below paddle.",
        "- Press ESC to exit to menu anytime.",
        "- Press 'P' to Pause/Resume the game.",
        "Press ENTER to return to menu."
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()

def reset_game():
    global paddle, ball, ball_speed_x, ball_speed_y, score, game_over, win, paused
    paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
    ball_speed_x, ball_speed_y = 4, -4
    score = 0
    game_over = False
    win = False
    paused = False
    create_bricks()

# Game State
game_state = "menu"  # can be: menu, instructions, game
score = 0
game_over = False
win = False
paused = False
reset_game()

# Main Loop
running = True
while running:
    clock.tick(FPS)

    if game_state == "menu":
        draw_menu()

    elif game_state == "instructions":
        draw_instructions()

    elif game_state == "game":
        screen.fill(BLACK)

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Ball movement (only if not paused or over)
        if not paused and not game_over and not win:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1
            if ball.colliderect(paddle):
                ball_speed_y *= -1

            for brick in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove(brick)
                    ball_speed_y *= -1
                    score += 10
                    break

            if ball.bottom >= HEIGHT:
                game_over = True
            if not bricks:
                win = True

        # Draw elements
        for brick in bricks:
            pygame.draw.rect(screen, BLUE, brick)
        pygame.draw.rect(screen, GREEN, paddle)
        pygame.draw.circle(screen, RED, (ball.centerx, ball.centery), ball_radius)

        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Pause/Resume Display
        if paused and not game_over and not win:
            pause_text = font.render("Game Paused. Press 'P' to Resume.", True, GRAY)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        # Game Over / Win Display
        if game_over:
            msg = font.render("Game Over! Press ESC to Menu.", True, RED)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        elif win:
            msg = font.render("You Win! Press ESC to Menu.", True, GREEN)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    # Handle events (all states)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    reset_game()
                    game_state = "game"
                elif event.key == pygame.K_2:
                    game_state = "instructions"
                elif event.key == pygame.K_3:
                    running = False

        elif game_state == "instructions":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "menu"

        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                elif event.key == pygame.K_p and not game_over and not win:
                    paused = not paused  # Toggle pause

pygame.quit()
