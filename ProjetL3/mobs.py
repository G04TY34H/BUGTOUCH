import pygame
import function as f

import random
import time

class mobs_class:
    def __init__(self,selected_time_value):

        self.list_mobs = []  # List contenant tous les mobs moskito, moskigros et piou
        self.game_start_time = time.time()  # Timer pour faire un intervalle entre chaque spawn de mob
        self.insects_spawn_timer = 2    # 2 Sec entre chaque spawn de base
        self.moskito_spawn_time = 2
        self.time = selected_time_value  # Time_Value équivalent au temps sélectionné dans Choix Mode de Jeu, =0 si Mode sans Temps

        self.score_value_mobs = 0   # Score

    def spawn_insects(self):
        t = time.time()
        if t > self.insects_spawn_timer:  # Si 't' > timer spawn mob alors spawn mob
            self.insects_spawn_timer = t + self.moskito_spawn_time

            if self.time != 0:  # Si == 0 alors mode sans temps sélectionné
                nb = (self.time - self.time_left) / self.time * 100 / 2  # % spawn Piou augmentant au fur et à mesure de la parti
            else:
                nb = 20     # Nb correspond au pourcentage de chance de faire spawner un Piou

            if random.randint(0, 100) < nb:  # Si % chance spawn piou < au chiffre généré alors spawn piou
                self.list_mobs.append(piou())
            elif random.randint(0,100) > 50:  # Sinon spawn un moskito, 50% de chance d'avoir un Moskigros, 50% un moskito
                self.list_mobs.append(moskito())    # Spawn Moskito
            else:
                self.list_mobs.append(moskigros())  # Spawn Moskigros

    def update_mobs(self, window):  # Méthode Update de la class mobs

        x_ball, y_ball = f.get_ball_coord(window.get_width(), window.get_height())  # Récupération coordonnées Balles

        self.game_time_update()  # MAJ du timer interne à la classe mob
        self.spawn_insects()    # Méthode spawn mob

        for mob in self.list_mobs:  # Pour tous les mobs présents dans la liste
            mob.draw(window)    # Affiche les mobs vis la méthode draw

        if self.time_left > 0:  # Si temps restant > 0 alors parti toujours en cours
            self.spawn_insects()    #
            for mob in self.list_mobs:  # Pour tous les mobs
                if mob.hitbox.collidepoint(x_ball, y_ball) and x_ball >= 0 and y_ball >= 0:  # Check SI impact avec Balle
                    f.sound_manager.play(mob.death_sound)
                    self.score_value_mobs += mob.point_value    # SI impact alors ajoute montant de point(s) lié au mob touché
                    self.list_mobs.remove(mob)  # Supprime le mob touché      | 1pt Mokigros | 2pts Moskito | -1pt Piou
                else:
                    mob.move()  # Si mob pas touchée alors on le fait se déplacer


    def game_time_update(self):  # Update du décompte interne à la class mob
        if self.time != 0:
            self.time_left = max(round(self.time - (time.time() - self.game_start_time), 1), 0)
        else:
            self.time_left = max(round(10000 - (time.time() - self.game_start_time), 1), 0)

    def get_score_value(self):  # Getter du Score pour IHM
        return self.score_value_mobs

class moskito:  # CLASS MOSKITO
    def __init__(self):

        moving_direction, start_pos = self.define_spawn_pose((125,125))  # Détermine direction et position de départ

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.death_sound = "kill_moskito"
        self.point_value = 2    # Valeur de pts donnée par le moskito
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],125,125)   # Initialization HitBox du moskito

        if f.selected_color == 'red':
            self.images = f.image_resize(150, 150, r'Moskito_violet.png')
        else:
            self.images = f.image_resize(150, 150, r'Moskito.png')

        self.images = pygame.transform.flip(self.images, bool_flip, False)  # Flip l'image du moskito dépendamment de sa direction

    def define_spawn_pose(self, size):  # Défini l'emplacement de départ du moskito et sa vitesse de déplacement
        vel = random.uniform(1, 2) # Vitesse des mobs allant de 1 à 2
        moving_direction = random.choice(("left", "right", "up", "down"))   # Choix entre les 4 côtés de la fenêtre
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
        return moving_direction, start_pos  # Renvoi la direction du moskito et sa vitesse

    def move(self):  # Méthode faisant déplacer les moskitos
        self.hitbox.move_ip(self.vel)

    def draw(self, window):  # Affiche les moskitos
        draw(window, self.images, self.hitbox.center, pos_mode="center")


def draw(surface, img, pos, pos_mode="top_left"):   # Méthodes Draw
    if pos_mode == "center":    # SI pos == Center, change la position de l'image pour match le centre
        pos = list(pos)
        pos[0] -= img.get_width()//2
        pos[1] -= img.get_height()//2

    surface.blit(img, pos)  # Affichage de l'image sur la fenêtre du jeu

class moskigros(moskito):   # CLASS MOSKIGROS AVEC HERITAGE MOSKITO
    def __init__(self):
        
        moving_direction, start_pos = self.define_spawn_pose((250,250))  # Détermine direction et position de départ

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.death_sound = "kill_moskito"
        self.point_value = 1    # Valeur de pts donnée par le moskito
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],250,250)    # Initialization HitBox du moskito

        if f.selected_color == 'red':
            self.images = f.image_resize(200, 200, r'Moskigros_violet.png')
        else:
            self.images = f.image_resize(200, 200, r'Moskigros.png')

        self.images = pygame.transform.flip(self.images, bool_flip, False)


class piou(moskito):    # CLASS PIOU AVEC HERITAGE MOSKITO
    def __init__(self):
        
        moving_direction, start_pos = self.define_spawn_pose((100,100))  # Détermine direction et position de départ

        if moving_direction == "left":
            bool_flip = True
        else:
            bool_flip = False

        self.death_sound = "kill_moskito"
        self.point_value = -1   # Valeur de pts donnée par le moskito
        self.hitbox = pygame.Rect(start_pos[0], start_pos[1],100,100)    # Initialization HitBox du moskito
        self.images = f.image_resize(100, 100, r'Piou_Rose.png')  # Initialise Image du Moskito
        self.images = pygame.transform.flip(self.images, bool_flip, False)  # Flip l'image du moskito dépendamment de sa direction
