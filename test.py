import pygame
import sys
pygame.init()
HEIGHT = 900
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load('Backgroung.jpg')
screen.blit(bg, (0,0))

MENU_HEIGHT = 300
MENU_WIDTH = 200

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

sound3 = pygame.mixer.Sound('Erich-Weinert-Ensemble_-_Arbeiter_von_Wien_(musmore.com).mp3')
sound2 = pygame.mixer.Sound('Rammstein Links 2-3-4.mp3')
sound1 = pygame.mixer.Sound('mechanic-button-pressing_fj_hbhno.mp3')

menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
menu = pygame.image.load('menu.png')
menu_surface.blit(menu, (0, 0))
screen.blit(menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

button1 = pygame.image.load('singleplayer.png')
screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

button2 = pygame.image.load('options.png')
screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 350))

button3 = pygame.image.load('quit.png')
screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 390))

pygame.display.update()
clock = pygame.time.Clock()

def quit(event):
    if event.type == pygame.QUIT:
        return True
    else:
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = event.pos
            if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
                                                                    (y > 390 and y < 415)):
                return True

def chose_music(event):

    if event.type == pygame.MOUSEBUTTONDOWN :
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 350, y < 375):
            pass


def volume(event):
    pass


Finished = False
while not Finished:

    clock.tick(FPS)
    EVENTS = pygame.event.get()

    for event in EVENTS:

        Finished = quit(event)
        chose_music(event)
        volume(event)

        if event.type == pygame.QUIT:
            Finished = True
        
    '''
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Finished = True
 
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_1:
                sound3.stop()
                sound3.play()

            elif i.key == pygame.K_MINUS:
                sound3.set_volume(0.5)

            elif i.key == pygame.K_EQUALS:
                sound3.set_volume(1)
 
        elif i.type == pygame.MOUSEBUTTONUP:
            if i.button == 1:
                sound1.play()
            elif i.button == 3:
                sound1.stop()
                sound2.play()
 
    
    pygame.display.update()
    screen.fill(WHITE)
    '''
