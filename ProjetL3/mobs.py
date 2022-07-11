import pygame
import function as f

import random
import time


class mobs_class:
    def __init__(self,selected_time_value):

        self.list_mobs=[]
        self.game_start_time = time.time()
        self.insects_spawn_timer = 2
        self.moskito_spawn_time = 2
        self.time = selected_time_value

        self.score_value_mobs = -1

    def spawn_insects(self):
        t = time.time()
        if t > self.insects_spawn_timer:
            self.insects_spawn_timer = t + self.moskito_spawn_time

            if self.time != 0:
                nb = (self.time - self.time_left) / self.time * 100 / 2
            else:
                nb = 20

            if random.randint(0, 100) < nb:
                self.list_mobs.append(piou())
            elif random.randint(0,100)>50:
                self.list_mobs.append(moskito())
            else:
                self.list_mobs.append(moskigros())

    def update_mobs(self, window):

        x_ball, y_ball = f.get_ball_coord(window.get_width(), window.get_height())

        self.game_time_update()
        self.spawn_insects()

        for mob in self.list_mobs:
            mob.draw(window)

        if self.time_left > 0:
            self.spawn_insects()
            for mob in self.list_mobs:
                if mob.hitbox.collidepoint(x_ball, y_ball) and x_ball >= 0 and y_ball >= 0:
                    self.score_value_mobs += mob.point_value
                    self.list_mobs.remove(mob)
                else:
                    mob.move()


    def game_time_update(self):
        if self.time != 0:
            self.time_left = max(round(self.time - (time.time() - self.game_start_time), 1), 0)
        else :
            self.time_left = max(round(10000 - (time.time() - self.game_start_time), 1), 0)

    def get_score_value(self):
        return(self.score_value_mobs)



class moskito:
    def __init__(self):

        moving_direction, start_pos = self.define_spawn_pose((125,125))

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.point_value = 2
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],125,125)
        self.images = f.image_resize(125, 125, r'Ressources/Moskito_violet.png')
        self.images = pygame.transform.flip(self.images, bool_flip, False)




    def define_spawn_pose(self, size): # define the start pos and moving vel of the mosquito
        vel = random.uniform(1, 2)
        moving_direction = random.choice(("left", "right", "up", "down"))
        if moving_direction == "right":
            start_pos = (-size[0], random.randint(size[1], 720-size[1]))
            self.vel = [vel, 0]
        if moving_direction == "left":
            start_pos = (1280 + size[0], random.randint(size[1], 720-size[1]))
            self.vel = [-vel, 0]
        if moving_direction == "up":
            start_pos = (random.randint(size[0], 1280-size[0]), 720+size[1])
            self.vel = [0, -vel]
        if moving_direction == "down":
            start_pos = (random.randint(size[0], 1280-size[0]), -size[1])
            self.vel = [0, vel]
        return moving_direction, start_pos

    def move(self):
        self.hitbox.move_ip(self.vel)

    def draw(self, window):
        draw(window, self.images, self.hitbox.center, pos_mode="center")


def draw(surface, img, pos, pos_mode="top_left"):
    if pos_mode == "center":
        pos = list(pos)
        pos[0] -= img.get_width()//2
        pos[1] -= img.get_height()//2

    surface.blit(img, pos)


class moskigros(moskito):
    def __init__(self):
        
        moving_direction, start_pos = self.define_spawn_pose((250,250))

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.point_value = 1
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],250,250)
        self.images = f.image_resize(200, 200, r'Ressources/Moskigros_violet.png')
        self.images = pygame.transform.flip(self.images, bool_flip, False)


class piou(moskito):
    def __init__(self):
        
        moving_direction, start_pos = self.define_spawn_pose((100,100))

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.point_value = -1
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],100,100)
        self.images = f.image_resize(100, 100, r'Ressources/Piou_Rose.png')
        self.images = pygame.transform.flip(self.images, bool_flip, False)
