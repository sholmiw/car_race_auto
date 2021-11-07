import pygame,pygame.mixer
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()
import cars

pygame.init()
#music = pygame.mixer.music.load('boom.wav')

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (195, 250)

CAR_SCALE = 0.25 # 0.55
RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), CAR_SCALE)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), CAR_SCALE)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60
player_car = cars.PlayerCar(4, 4,RED_CAR)
frontSense = cars.sensor(player_car,player_car.x,player_car.y,70)
leftSense = cars.sensor(player_car,player_car.x,player_car.y,70,offsetSensor=45)
rigthSense = cars.sensor(player_car,player_car.x,player_car.y,70,offsetSensor=-45)
def draw(win, images):
    for img, pos in images:
        win.blit(img, pos)
    ##########
    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))
    ##########
    player_car.draw(win)
    frontSense.draw(win)
    leftSense.draw(win)
    rigthSense.draw(win)
    pygame.display.update()

reset = False
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION)]

def handle_collision(object):
    if object.collide(TRACK_BORDER_MASK) != None:
        print("boom! we have a collision")
        #music.play('boom.wav')
        object.bounce()

while run:
    clock.tick(FPS)
    draw(WIN, images)

    #############
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset = True
        player_car.reset()
        reset = False
    if not reset:
        cars.move_player(player_car)
        handle_collision(player_car)
        #print(player_car.vel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

pygame.quit()

#2 parts
"""
1: set window
2: compute new window
"""