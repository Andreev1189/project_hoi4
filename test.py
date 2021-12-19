import pygame

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
sound3 = pygame.mixer.Sound('mechanic-button-pressing_fj_hbhno.mp3')

menu_type = 'main'

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
    print(12)

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
    print(9)

def draw_audio_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):

    audio_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('menu.png')
    audio_menu_surface.blit(menu, (0, 0))
    screen.blit(audio_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('first.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('second.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 390))

    button3 = pygame.image.load('Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )

def draw_game_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):

    game_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('menu.png')
    game_menu_surface.blit(menu, (0, 0))
    screen.blit(game_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button3 = pygame.image.load('Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )
    '''
    сюда надо вставить пасту
    '''

draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)


def quit_main(event):

    if event.type == pygame.QUIT:
        return True
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
                                                                    (y > 550 and y < 575)):
                return True


def quit(event):
    if event.type == pygame.QUIT:
        return True

def click_sound_effect(event, sound3):

    if event.type == pygame.MOUSEBUTTONDOWN:
        sound3.play()

def play_music(event, current_sound, sound1, sound2):

    if current_sound == sound2:
        sound2.stop()
        sound1.play()
    elif current_sound == sound1:
        sound1.stop()
        sound2.play()

def chose_music(event, current_sound, sound1, sound2):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            (y > 310 and y < 375)):

            if current_sound == sound2:
                current_sound = sound1

            play_music(event, current_sound, sound1, sound2)    

        elif(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            (y > 390 and y < 390 + 65)):

            if current_sound == sound1:
                current_sound = sound2

            play_music(event, current_sound, sound1, sound2)

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



def main_to_option(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 350 and y < 375):
            return True


def option_to_main(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 530 and y < 583):
            return True

def option_to_game(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 310 and y < 370):
            return True

def game_to_option(event):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 530 and y < 583 ):
            return True

def option_to_audio(event):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 380 and y < 440):
            return True

def audio_to_option(event):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 530 and y < 583):
            return True

pygame.display.update()
clock = pygame.time.Clock()

Finished = False

while not Finished:

    clock.tick(FPS)
    EVENTS = pygame.event.get()

    for event in EVENTS:
        
        if menu_type == 'audio':

            if audio_to_option(event):
                menu_type = 'option'
                draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            current_sound = chose_music(event, current_sound, sound1, sound2)
            volume = Volume(event, volume)
            sound1.set_volume(volume)
            sound2.set_volume(volume)

            click_sound_effect(event, sound3)
            Finished = quit(event)
    

  
        elif menu_type == 'option':

            Finished = quit(event)

            if option_to_main(event):
                menu_type = 'main'
                draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            if option_to_game(event):
                menu_type = 'game'
                draw_game_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            if option_to_audio(event):
                menu_type = 'audio'
                draw_audio_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            click_sound_effect(event, sound3)
            
    
        elif menu_type == 'main':


            Finished = quit_main(event)

            if main_to_option(event):
                menu_type = 'option'
                draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)
                print(10)

            click_sound_effect(event, sound3)
            print('I m here')

        elif menu_type == 'game':

            Finished = quit(event)

            if game_to_option(event):
                menu_type = 'option'
                draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            click_sound_effect(event, sound3)
           
    pygame.display.update()
    print(menu_type)


        
# 1/2 68 - 70