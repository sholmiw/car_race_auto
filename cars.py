from utils import scale_image, blit_rotate_center, blit_text_center
import time
import math
import pygame

CAR_FULL_SIZE_X =38
CAR_FULL_SIZE_Y =76
CAR_SCALE = 0.25

class AbstractCar:
    def __init__(self, max_vel, rotation_vel,img):
        self.img = img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0 # car facing north/up the screen
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.offsetX  = CAR_FULL_SIZE_X * CAR_SCALE * 0.5 # 10 # the width of the car is 20 px
        self.offsetY = CAR_FULL_SIZE_Y * CAR_SCALE * 0.5 # 23 the length of the car is ~50 px

    def getX_Y(self):
        return self.x,self.y

    def getOffset(self):
        return self.offsetX,self.offsetY

    def get_angle(self):
        return self.angle

    def reset(self):
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        #print (poi)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    START_POS = (180, 200)
    def __init__(self, max_vel, rotation_vel, pic):
        super().__init__(max_vel, rotation_vel, pic)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        #self.vel = -self.vel
        self.vel = 0
        self.move()

    #def auto_mood(self):
        pass


class ComputerCar(AbstractCar):

    def __init__(self, max_vel, rotation_vel, pic, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
        IMG = pic
        START_POS = (150, 200)

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0



def move_player(player_car,ACTIVEMOD = True):
    if ACTIVEMOD:
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        if keys[pygame.K_d]:
            player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            player_car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            player_car.move_backward()
        if not moved:
            player_car.reduce_speed()
    else:
        #use alg to move the car
        pass

class sensor():
    def __init__(self, car, posX, posY, length, offsetSensor=0):
        self.offsetSensor = offsetSensor + 90  # we have a 90 degree offset when we start
        self.faceing = car.get_angle()
        self.length = length
        self.x= posX
        self.y= posY
        self.car = car
        self.point_x =0
        self.point_y =0

    def calc(self):
        x,y = self.car.getX_Y()
        self.faceing = self.car.get_angle() +self.offsetSensor
        radians = math.radians(self.faceing)
        #print(self.faceing)

        desired_point_x_length = math.cos(radians)*self.length
        desired_point_y_length = math.sin(radians)*self.length *-1
        self.point_x = int(desired_point_x_length) + x
        self.point_y = int(desired_point_y_length) + y

    def collide(self, mask, x=0, y=0):
        sensor_mask = pygame.mask.from_surface()
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(sensor_mask, offset)
        # print (poi)
        return poi


    def draw(self, win):
        self.calc()
        x, y = self.car.getX_Y()
        offX, offY = self.car.getOffset()
        pygame.draw.circle(win, (255, 0, 0), (self.point_x+offX,self.point_y+offY), 5)
        pygame.draw.line(win, (255, 0, 0),(x+offX,y+offY),(self.point_x+offX,self.point_y+offY))
        #print(self.point_x,self.point_y)