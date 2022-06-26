import pygame, random, sys
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((1280, 720), HWSURFACE | DOUBLEBUF | RESIZABLE)
cursor = pygame.image.load(r'cursor.png')
cursor = pygame.transform.scale(cursor,(50,50))
background = pygame.image.load(r'fond.png')
pygame.display.set_caption("Insect Touch")

window.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))

pygame.mouse.set_visible(False)

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"font.ttf", size)

def show_score(x,y,score_value):

    score = get_font(60).render("Score : "+str(score_value), True,"#b68f40")
    window.blit(score,(x,y))

def main_menu(window): # Menu du Jeu

    pygame.display.set_caption("Menu")

    while True:

        MENU_TEXT = get_font(100).render("BUG Touch", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((window.get_width()/2), window.get_height()/9))
        MENU_BACKGROUND_IMAGE = pygame.image.load(r'Play Rect.png')
        MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND_IMAGE,(950,125))

        BOUTTON_JOUER = Button(image=pygame.image.load(r'Play Rect.png'),pos=((window.get_width()/2),window.get_height()/2-125),
                               text_input='JOUER', font=get_font(50),base_color="#d7fcd4", hovering_color="White")
        BOUTTON_REGLES = Button(image=pygame.image.load(r'Play Rect.png'), pos=((window.get_width()/2), window.get_height()/2+25),
                                text_input="REGLES", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        BOUTTON_QUITTER = Button(image=pygame.image.load(r'Play Rect.png'), pos=((window.get_width()/2), window.get_height()/2+175),
                             text_input="QUITTER", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_BACKGROUND,((window.get_width()/2)/4, (window.get_height()/2)/30))
        window.blit(MENU_TEXT,MENU_RECT)

        for button in [BOUTTON_JOUER,  BOUTTON_REGLES, BOUTTON_QUITTER]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == VIDEORESIZE:
                if window.get_width()<1152:
                    window = pygame.display.set_mode((1152,window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height()<648:
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
                    pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOUTTON_JOUER.checkForInput(pygame.mouse.get_pos()):
                    jouer(window)
                if BOUTTON_REGLES.checkForInput(pygame.mouse.get_pos()):
                    regles(window)
                if BOUTTON_QUITTER.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))


def jouer(window):

    SCORE_BACKGROUND_IMAGE = pygame.image.load(r'Play Rect.png')
    SCORE_BACKGROUND = pygame.transform.scale(SCORE_BACKGROUND_IMAGE, (700,85))

    score_value = 0
    rect = pygame.Rect(60, 60, 60, 60);

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(window)

            elif event.type == VIDEORESIZE:
                if window.get_width()<1152:
                    window = pygame.display.set_mode((1152,window.get_height()), pygame.RESIZABLE)
                    pygame.display.update()
                elif window.get_height()<648:
                    window = pygame.display.set_mode((window.get_width(), 648), pygame.RESIZABLE)
                    pygame.display.update()
                else:
                    window = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    window.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
                    pygame.display.update()

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if rect.collidepoint(event.pos):
                    x = random.randrange(window.get_width())
                    y = random.randrange(window.get_height())
                    rect.center = (x, y);
                    score_value += 1
                elif rect.x > window.get_width() or rect.y > window.get_height():
                    x = random.randrange(window.get_width())
                    y = random.randrange(window.get_height())
                    rect.center = (x, y);


        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))

        pygame.draw.circle(window, (255, 255, 0), rect.center, 50, 50)
        window.blit(SCORE_BACKGROUND, ((window.get_width() / 120), window.get_height() / 50))
        show_score(30, 30,score_value)

        window.blit(cursor, pygame.mouse.get_pos())
        pygame.display.update()

def regles(window):

    while True:

        fond_RETOUR = pygame.image.load(r'Play Rect.png')

        BOUTTON_RETOUR = Button(image=pygame.transform.scale(fond_RETOUR, (300,100)),
                                pos=((window.get_width() / 7.75), window.get_height() / 1.1 ),
                                text_input='RETOUR', font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        BOUTTON_RETOUR.changeColor(pygame.mouse.get_pos())
        BOUTTON_RETOUR.update(window)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(window)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOUTTON_RETOUR.checkForInput(pygame.mouse.get_pos()):
                    main_menu(window)

        window.blit(cursor, pygame.mouse.get_pos())

        pygame.display.update()
        window.blit(pygame.transform.scale(background, (window.get_width(), window.get_height())), (0, 0))

main_menu(window)

