import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

# Colors
BLACK = (15, 18, 25)
GREEN = (50, 220, 100)
DARK_GREEN = (25, 150, 70)
RED = (255, 65, 80)
WHITE = (255, 255, 255)
GRAY = (35, 40, 50)

def reset():
    snake = [(300, 300), (280, 300), (260, 300)]
    direction = (CELL, 0)

    food = (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

    return snake, direction, food, 0, False

snake, direction, food, score, game_over = reset()

running = True
move_timer = 0
speed = 110

# Prevent multiple turns between movements
can_turn = True

while running:
    dt = clock.tick(60)
    move_timer += dt

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, game_over = reset()
                can_turn = True
                move_timer = 0

            # Only allow one turn per movement
            if not game_over and can_turn:

                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                    can_turn = False

                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                    can_turn = False

                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                    can_turn = False

                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)
                    can_turn = False

    # Snake movement
    if not game_over and move_timer >= speed:

        move_timer = 0
        can_turn = True

        head = (
            snake[0][0] + direction[0],
            snake[0][1] + direction[1]
        )

        eating = head == food

        body = snake if eating else snake[:-1]

        # Collision detection
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in body
        ):
            game_over = True

        else:
            snake.insert(0, head)

            # Eat food
            if eating:
                score += 10

                while True:
                    food = (
                        random.randrange(0, WIDTH, CELL),
                        random.randrange(0, HEIGHT, CELL)
                    )

                    if food not in snake:
                        break

            else:
                snake.pop()

    # Draw background
    screen.fill(BLACK)

    # Draw grid
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw food
    pygame.draw.circle(
        screen,
        RED,
        (food[0] + CELL // 2, food[1] + CELL // 2),
        CELL // 2 - 2
    )

    # Draw snake
    for i, part in enumerate(snake):

        color = GREEN if i == 0 else DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            (part[0] + 1, part[1] + 1, CELL - 2, CELL - 2),
            border_radius=5
        )

    # Draw score
    score_text = font.render(
        "SCORE: " + str(score),
        True,
        WHITE
    )

    screen.blit(score_text, (15, 15))

    # Game over screen
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)

        screen.blit(overlay, (0, 0))

        title = font.render("GAME OVER!", True, RED)
        final = font.render("Score: " + str(score), True, WHITE)

        restart = small_font.render(
            "Press R to restart",
            True,
            GREEN
        )

        quit_text = small_font.render(
            "Press ESC to quit",
            True,
            WHITE
        )

        screen.blit(title, title.get_rect(center=(300, 240)))
        screen.blit(final, final.get_rect(center=(300, 290)))
        screen.blit(restart, restart.get_rect(center=(300, 350)))
        screen.blit(quit_text, quit_text.get_rect(center=(300, 385)))

    pygame.display.flip()

pygame.quit()
sys.exit()