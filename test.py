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

sound2 = pygame.mixer.Sound('Erich-Weinert-Ensemble_-_Arbeiter_von_Wien_(musmore.com).mp3')
sound1 = pygame.mixer.Sound('Rammstein Links 2-3-4.mp3')
sound5 = pygame.mixer.Sound('mechanic-button-pressing_fj_hbhno.mp3')

current_sound = sound2
volume = 0.5

def draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):

    main_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('menu.png')
    main_menu_surface.blit(menu, (0, 0))
    screen.blit(main_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('singleplayer.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('options.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 350))

    button3 = pygame.image.load('quit.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 550))

def draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):

    option_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('menu.png')
    option_menu_surface.blit(menu, (0, 0))
    screen.blit(option_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('Game.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('Audio.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 380) )

    button3 = pygame.image.load('Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )

draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)
draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

def quit(event):

    if event.type == pygame.QUIT:
        return True
    else:
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = event.pos
            if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
                                                                    (y > 550 and y < 575)):
                return True


def click_sound_effect(event, sound5):

    if event.type == pygame.MOUSEBUTTONDOWN:
        sound5.play()

def play_music(event, current_sound, sound1, sound2):

    if event.type == pygame.MOUSEBUTTONDOWN :
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 350, y < 375):
            if current_sound == sound2:
                sound2.stop()
                sound1.play()
            elif current_sound == sound1:
                sound1.stop()
                sound2.play()

def chose_music(event, current_sound, sound1, sound2):

    if event.type == pygame.MOUSEBUTTONDOWN :
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            (y > 350 and y < 375)):
            if current_sound == sound1:
                current_sound = sound2
            elif current_sound == sound2:
                current_sound = sound1

            play_music(event, current_sound,sound1, sound2)
            return current_sound

    return current_sound

def Volume(event, volume):

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_EQUALS:
            if volume < 1:
                volume += 0.1
        if event.key == pygame.K_MINUS:
            if volume > 0:
                volume -= 0.1
        
    return volume

def chaging_volume(volume, current_sound, sound1, sound2):
    
    if current_sound == sound1:
        sound1.set_volume(volume)
    if current_sound == sound2:
        sound1.set_volume(volume)

pygame.display.update()
clock = pygame.time.Clock()

Finished = False

while not Finished:

    clock.tick(FPS)
    EVENTS = pygame.event.get()

    for event in EVENTS:

        Finished = quit(event)
        click_sound_effect(event, sound5)
        current_sound = chose_music(event, current_sound, sound1, sound2)
        #play_music(event, current_sound,sound1, sound2)
        volume = Volume(event, volume)
        #chaging_volume(volume, current_sound, sound1, sound2)
        sound1.set_volume(volume)
        sound2.set_volume(volume)


        if event.type == pygame.QUIT:

            Finished = True
