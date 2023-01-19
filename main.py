import time
import pygame
import random

WIDTH = 1280
HEIGHT = 620
SPEED = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

balloon_surf = pygame.image.load('img/balloon.png').convert_alpha()
balloons_rect = []

flowncontrol = 0
flownvalue = True

timer = 0
start_time = pygame.time.get_ticks()
GAME_TIME = 8000
max_ballons = 10
for _ in range(max_ballons):
    balloon_rect = balloon_surf.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(150, HEIGHT - 50)))
    balloons_rect.append(balloon_rect)

bird = pygame.image.load('img/crosshair.png').convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))
score = 0
bird_x = WIDTH / 2
bird_y = HEIGHT / 2
bird_index = 0
bird_rect = bird.get_rect(center=(bird_x, bird_y))

counter = 0
forward = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            bird_rect = bird.get_rect(center=event.pos)

    keys = pygame.key.get_pressed()
    """
    #respawn
    for index, balloon_rect in enumerate(balloons_rect):
        if balloons_rect[index].right >= WIDTH:
            balloons_rect[index].right=(random.randint(50, WIDTH - 50))
            balloons_rect[index].right=(random.randint(50, HEIGHT - 150))
        elif balloons_rect[index].left <= 0:
            balloons_rect[index].right = (random.randint(50, WIDTH - 50))
            balloons_rect[index].right = (random.randint(50, HEIGHT - 150))
        elif balloons_rect[index].top <= 0:
            balloons_rect[index].right = (random.randint(50, WIDTH - 50))
            balloons_rect[index].right = (random.randint(50, HEIGHT - 150))
        elif balloons_rect[index].bottom >= HEIGHT:
            balloons_rect[index].right = (random.randint(50, WIDTH - 50))
            balloons_rect[index].right = (random.randint(50, HEIGHT - 150))
    """     
    # delete
    for index, balloon_rect in enumerate(balloons_rect):
        if balloons_rect[index].right >= WIDTH:
            del balloons_rect[index]
        elif balloons_rect[index].left <= 0:
            del balloons_rect[index]
        elif balloons_rect[index].top <= 0:
            del balloons_rect[index]
        elif balloons_rect[index].bottom >= HEIGHT:
            del balloons_rect[index]
    screen.fill((140, 137, 246))

    # flowncontrol
    for index, balloon_rect in enumerate(balloons_rect):
        balloons_rect[index].top -= 1
        if flownvalue and flowncontrol <= 150:
            balloons_rect[index].left += 1
            flowncontrol += 1
        elif flownvalue and flowncontrol > 150:
            flownvalue = False
        elif not flownvalue and flowncontrol >= 0:
            balloons_rect[index].left -= 1
            flowncontrol -= 1
        elif not flownvalue and flowncontrol < 0:
            flownvalue = True
    """
    #radomized_movement
    mov_y = random.randint(0, 3)
    if mov_y == 0:
        balloons_rect[index].left -= 2
    else:
        balloons_rect[index].left += 2
    """

    # score
    for index, balloon_rect in enumerate(balloons_rect):
        if balloon_rect.colliderect(bird_rect) and pygame.mouse.get_pressed()[0]:
            score += 1
            del balloons_rect[index]
        else:
            screen.blit(balloon_surf, balloon_rect)
    # timer
    time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
    game_font = pygame.font.SysFont('arial', 60)
    timer_surf = game_font.render('Time: ' + str(time_left), True, (255, 0, 0))
    score_surf = game_font.render('Score: ' + str(score), True, (255, 0, 0))

    # ending
    winning_surf = game_font.render('', True, (255, 0, 0))
    if time_left == 0:
        winning_surf = game_font.render('Time ran out', True, (255, 0, 0))
        screen.blit(winning_surf, (320, 320))
        running = False
        time.sleep(2)
    elif balloons_rect == []:
        if score == max_ballons:
            winning_surf = game_font.render('You won', True, (255, 0, 0))
            screen.blit(winning_surf, (320, 320))
            running = False
        elif score != max_ballons:
            winning_surf = game_font.render('You didnt got all of them', True, (255, 0, 0))
            screen.blit(winning_surf, (320, 320))
            running = False

    screen.blit(score_surf, (0, 0))
    screen.blit(timer_surf, (0, 560))
    screen.blit(winning_surf, (320, 320))
    screen.blit(bird, bird_rect)
    pygame.display.update()
    clock.tick(60)
time.sleep(2)
pygame.quit()
