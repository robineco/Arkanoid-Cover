import random
import sys

import pygame
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

GREEN = (0, 255, 0)
ORANGE = (255, 144, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUEISH = (17, 86, 143)
RED = (255, 0, 0)

WIDTH = 400
HEIGHT = 400
BAR_WIDTH = 60
BAR_HEIGHT = 15
BALL_RADIUS = 10

ball_pos = [0, 0]
ball_velocity = [0, 0]
bonus_box = []
score = 0

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Unknown Game Name")

ball = pygame.draw.circle(window, BLUEISH, ball_pos, BALL_RADIUS, 0)
bar = pygame.draw.rect(window, BLACK, Rect(170, 370, BAR_WIDTH, BAR_HEIGHT), 0)


def init_ball():
    global ball_pos, ball_velocity
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    x_velocity = random.uniform(2, 6)
    y_velocity = random.uniform(2, 5)

    ball_velocity = [x_velocity, y_velocity]
    print(ball_velocity)


def init_bonus():
    global bonus_box
    for i in range(random.randint(3, 13)):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        bonus = pygame.draw.rect(
            window,
            (red, green, blue),
            Rect(random.randint(15, WIDTH - 20), random.randint(15, HEIGHT - 100), 15, 15),
            0)
        bonus_box.append(bonus)


def final_text(complete):
    ball_velocity[0] = 0
    ball_velocity[1] = 0
    font = pygame.font.SysFont("Arial", 36)
    if complete:
        text = font.render("Level Complete!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        window.blit(text, text_rect)
    else:
        text = font.render("Failed", True, RED)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        window.blit(text, text_rect)


def draw_elements():
    global ball_pos, ball_velocity, ball, bar, bonus_box, score

    window.fill(WHITE)

    # wall bounce
    if ball_pos[0] >= (WIDTH - BALL_RADIUS) or ball_pos[0] <= BALL_RADIUS:
        ball_velocity[0] *= (-1)
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS) or ball_pos[1] <= BALL_RADIUS:
        ball_velocity[1] *= (-1)

    # ball under bar
    if ball_pos[1] > 380:
        final_text(False)

    # collision ball with bar
    if ball.colliderect(bar):
        ball_velocity[1] *= (-1.09)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_velocity[0] *= (-1.09)
        elif keys[pygame.K_RIGHT]:
            ball_velocity[0] *= (-1.09)
        else:
            ball_velocity[0] *= 1.09

    # collision wall with bonus box
    for bonus in bonus_box:
        if ball.colliderect(bonus):
            bonus_box.remove(bonus)
            score += 1
            ball_velocity[0] *= 1.1
            ball_velocity[1] *= 1.1

    # is level complete?
    if not bonus_box:
        final_text(True)

    # add velocity to ball
    ball_pos[0] += int(ball_velocity[0])
    ball_pos[1] += int(ball_velocity[1])

    # draw score & speed
    font = pygame.font.SysFont("Arial", 18)
    label = font.render('Score: ' + str(score), 1, BLACK)
    window.blit(label, (5, 5))
    label_speed = font.render('Speed: ' + str(round(ball_velocity[0], 2)), 1, BLACK)
    window.blit(label_speed, (5, 22))

    # draw elements
    ball = pygame.draw.circle(window, BLUEISH, ball_pos, BALL_RADIUS, 0)
    bar = pygame.draw.rect(window, BLACK, bar, 0)
    for bonus in bonus_box:
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        pygame.draw.rect(window, (red, green, blue), bonus, 0)


def move_bar(left):
    global bar
    if left and bar.x > 0:
        bar.x -= 10
    elif bar.x < WIDTH - BAR_WIDTH:
        bar.x += 10


def main():
    print('starting')
    init_ball()
    init_bonus()

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_bar(True)
        if keys[pygame.K_RIGHT]:
            move_bar(False)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_elements()
        pygame.display.update()
        fps.tick(30)


if __name__ == '__main__':
    main()
