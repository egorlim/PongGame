import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

white = (255, 255, 255)
black = (0, 0, 0)

paddle_width = 10
paddle_height = 100
ball_size = 20

player1_x = 50
player1_y = screen_height // 2 - paddle_height // 2
player2_x = screen_width - 50 - paddle_width
player2_y = screen_height // 2 - paddle_height // 2

initial_ball_speed = 5
ball_x = screen_width // 2 - ball_size // 2
ball_y = screen_height // 2 - ball_size // 2
ball_dx = initial_ball_speed
ball_dy = initial_ball_speed

paddle_speed = 7

score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)
win_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 36)

speed_increment_interval = 3000  # Increase speed every 3000ms (3 seconds)
last_speed_increment_time = pygame.time.get_ticks()

pause_rect = pygame.Rect(screen_width // 2 - 50, 5, 100, 40)
paused = False
resume = False

def reset_ball(scored_by_left):
    global ball_x, ball_y, ball_dx, ball_dy, last_speed_increment_time
    ball_x = screen_width // 2 - ball_size // 2
    ball_y = screen_height // 2 - ball_size // 2
    ball_dx = initial_ball_speed if scored_by_left else -initial_ball_speed
    ball_dy = initial_ball_speed
    last_speed_increment_time = pygame.time.get_ticks()

def pause_game():
    global paused
    paused = True
    screen.fill(black)
    pause_text = font.render("Paused", True, white)
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))
    resume_text = button_font.render("Press SPACE to Resume", True, white)
    screen.blit(resume_text, (screen_width // 2 - resume_text.get_width() // 2, screen_height // 2 + pause_text.get_height()))
    pygame.display.flip()

def resume_game():
    countdown = 3
    while countdown > 0:
        screen.fill(black)
        countdown_text = font.render(str(countdown), True, white)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        countdown -= 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(event.pos):
            pause_game()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and paused:
            paused = False
            resume_game()

    if paused:
        pygame.time.Clock().tick(30)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player1_y > 0:
        player1_y -= paddle_speed
    if keys[pygame.K_z] and player1_y < screen_height - paddle_height:
        player1_y += paddle_speed
    if keys[pygame.K_k] and player2_y > 0:
        player2_y -= paddle_speed
    if keys[pygame.K_m] and player2_y < screen_height - paddle_height:
        player2_y += paddle_speed

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y <= 0 or ball_y >= screen_height - ball_size:
        ball_dy = -ball_dy

    if (ball_x <= player1_x + paddle_width and player1_y <= ball_y + ball_size and ball_y <= player1_y + paddle_height) or \
       (ball_x >= player2_x - ball_size and player2_y <= ball_y + ball_size and ball_y <= player2_y + paddle_height):
        ball_dx = -ball_dx

    if ball_x < 0:
        score2 += 1
        reset_ball(scored_by_left=False)
    elif ball_x > screen_width:
        score1 += 1
        reset_ball(scored_by_left=True)

    current_time = pygame.time.get_ticks()
    if current_time - last_speed_increment_time >= speed_increment_interval:
        ball_dx *= 1.1  
        ball_dy *= 1.1
        last_speed_increment_time = current_time

    screen.fill(black)
    pygame.draw.rect(screen, white, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_size, ball_size))
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

    score_text = font.render(f"{score1} - {score2}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 60))

    pygame.draw.rect(screen, white, pause_rect)
    pause_text = button_font.render("Pause", True, black)
    screen.blit(pause_text, (pause_rect.x + 10, pause_rect.y + 5))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

    if score1 == 10 or score2 == 10:
        winner = "Player 1" if score1 == 10 else "Player 2"
        running = False

screen.fill(black)
win_text = win_font.render(f"{winner} wins!", True, white)
screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - win_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
