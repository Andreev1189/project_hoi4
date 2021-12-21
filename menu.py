import pygame

pygame.init()
HEIGHT = 900
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load('pictures/Backgroung.jpg') # загружаем задний фон заставки в меню
screen.blit(bg, (0,0))

MENU_HEIGHT = 300
MENU_WIDTH = 200

FPS = 30

# загружаем музыку в соответствующие переменные

sound2 = pygame.mixer.Sound('music/Erich-Weinert-Ensemble_-_Arbeiter_von_Wien_(musmore.com).mp3')
sound1 = pygame.mixer.Sound('music/Rammstein Links 2-3-4.mp3')
sound3 = pygame.mixer.Sound('music/mechanic-button-pressing_fj_hbhno.mp3')

menu_type = 'main' # переменная меняющая свое значение при разных типах меню (main, option, audio, game)

current_sound = sound2 
volume = 0.5

def draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):
    '''
    функция строит интерфейс главного меню
    на вход получает:
    экран - screen
    размеры экрана HEIGHT, WIDTH
    первый блок - поверхность на которую накладываются кнопки, размеры - MENU_HEIGHT, MENU_HEIGHT

    второй блок - прикрепялем кнопку "singleplayer"
    третий блок - прикрепляем кнопку "options"
    четвертый блок - прикрепляем кнопку "quit"
    '''

    main_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('pictures/menu.png')
    main_menu_surface.blit(menu, (0, 0))
    screen.blit(main_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('pictures/singleplayer.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('pictures/options.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 350))

    button3 = pygame.image.load('pictures/quit.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 550))

def draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):
    '''
    функция строит интерфейс опционального меню
    на вход получает:
    экран - screen
    размеры экрана HEIGHT, WIDTH
    первый блок - поверхность на которую накладываются кнопки, размеры - MENU_HEIGHT, MENU_HEIGHT

    второй блок - прикрепялем кнопку "Game"
    третий блок - прикрепляем кнопку "Audio"
    четвертый блок - прикрепляем кнопку "Back"
    '''

    option_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('pictures/menu.png')
    option_menu_surface.blit(menu, (0, 0))
    screen.blit(option_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('pictures/Game.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('pictures/Audio.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 380) )

    button3 = pygame.image.load('pictures/Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )

def draw_audio_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):
    '''
    функция строит интерфейс меню аудио
    на вход получает:
    экран - screen
    размеры экрана HEIGHT, WIDTH
    первый блок - поверхность на которую накладываются кнопки, размеры - MENU_HEIGHT, MENU_HEIGHT

    второй блок - прикрепялем кнопку "первой песни"
    третий блок - прикрепляем кнопку "второй песни"
    четвертый блок - прикрепляем кнопку "назад"
    '''

    audio_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('pictures/menu.png')
    audio_menu_surface.blit(menu, (0, 0))
    screen.blit(audio_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button1 = pygame.image.load('pictures/first.png')
    screen.blit(button1, ((WIDTH - MENU_WIDTH)/2, 310))

    button2 = pygame.image.load('pictures/second.png')
    screen.blit(button2, ((WIDTH - MENU_WIDTH)/2, 390))

    button3 = pygame.image.load('pictures/Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )

def draw_game_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH):
    '''
    функция строит интерфейс меню аудио
    на вход получает:
    экран - screen
    размеры экрана HEIGHT, WIDTH
    первый блок - поверхность на которую накладываются кнопки, размеры - MENU_HEIGHT, MENU_HEIGHT

    второй блок - прикрепялем кнопку "назад"
    '''

    game_menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu = pygame.image.load('pictures/menu.png')
    game_menu_surface.blit(menu, (0, 0))
    screen.blit(game_menu_surface, ((WIDTH - MENU_WIDTH)/2, (HEIGHT - MENU_HEIGHT)/ 2))

    button3 = pygame.image.load('pictures/Back.png')
    screen.blit(button3, ((WIDTH - MENU_WIDTH)/2, 530) )
    '''
    сюда надо вставить пасту
    '''

draw_main_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)


def quit_main(event):
    '''
    получет на вход event

    запускается если находимся в главном меню
    проверяет нажали-ли на кнопку выхода или на крестик
    в положительном случает возвращает True
    '''

    if event.type == pygame.QUIT:
        return True
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
                                                                    (y > 550 and y < 575)):
                return True


def quit(event):
    '''
    получает на вход event
    функция проверяет нажалили ли мы на крестик
    в положительном случает возвращает True
    '''
    if event.type == pygame.QUIT:
        return True

def click_sound_effect(event, sound3):
    '''
    на вход принимает evevt, и композицию
    при нажатии на кнопку мыши создает звуковой эффект
    '''

    if event.type == pygame.MOUSEBUTTONDOWN:
        sound3.play()

def play_music(event, current_sound, sound1, sound2):
    '''
    воспроизводит две песни в зависимости он параметра current_sound 
    меняет композиции при нажатии в меню аудио на кнопки 1/2
    '''

    if current_sound == sound2:
        sound1.stop()
        sound2.stop()
        sound1.play()

    elif current_sound == sound1:
        sound2.stop()
        sound1.stop()
        sound2.play()

def chose_music(event, current_sound, sound1, sound2):
    '''
    на вход получает event, две песни и параметр current_sound
    функция определяет значениe current_sound
    и в случае изменения запускает новую композицию 
    по средству запуска функции play_music()
    возвращает значение текущей песни
    '''

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            (y > 310 and y < 375)):

            if current_sound == sound2:
                current_sound = sound1

            play_music(event, current_sound, sound1, sound2)    

        elif(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            (y > 390 and y < 455)):

            if current_sound == sound1:
                current_sound = sound2

            play_music(event, current_sound, sound1, sound2)

    return current_sound

def Volume(event, volume):
    '''
    функция получает на вход event и значение громкости звука(volume)
    при нажатии на + - изменяет громкость
    возвращает громкость
    '''

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_EQUALS:
            if volume < 1:
                volume += 0.1
        if event.key == pygame.K_MINUS:
            if volume > 0:
                volume -= 0.1
        
    return volume


def main_to_option(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 350 and y < 375):
            return True

def option_to_main(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if(( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and
            y > 530 and y < 583):
            return True

def option_to_game(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 310 and y < 370):
            return True

def game_to_option(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 530 and y < 583 ):
            return True

def option_to_audio(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 380 and y < 440):
            return True

def audio_to_option(event):
    '''
    получает на вход event
    функция переключает меню как в описано в названии
    при попадании кнопкой мыши на соответствующую кнопку
    '''
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if (( x > (WIDTH - MENU_WIDTH)/2 and x < (WIDTH - MENU_WIDTH)/2 + MENU_WIDTH) and 
            y > 530 and y < 583):
            return True

def GENERAL(event, sound1, sound2, sound3, current_sound, screen, HEIGHT, 
                                MENU_HEIGHT, WIDTH, MENU_WIDTH, menu_type, volume, Finished):
        
        '''
        функция выполняет всю логику программы в главном цикле
        функция получает на вход основные константы 
        а также изменяющиеся параметры:

        current_sound - текущая песня
        menu_type - тип текущего меню
        volume - уровень громкости
        Finished - проверка на завершенность главного цикла программы

        возвращает в том же порядке изменяющиеся параметры

        функция разделена на четыре блока (четыре типа окна меню)
        в каждом блоке описаны процессы которые необходимо проверять
        в соответствующем типе меню
        '''

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

            click_sound_effect(event, sound3)

        elif menu_type == 'game':

            Finished = quit(event)

            if game_to_option(event):

                menu_type = 'option'
                draw_option_menu(screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH)

            click_sound_effect(event, sound3)

        return current_sound, menu_type, volume, Finished

pygame.display.update()
clock = pygame.time.Clock()

Finished = False

while not Finished:

    clock.tick(FPS)
    EVENTS = pygame.event.get()

    for event in EVENTS:
        current_sound, menu_type, volume, Finished = GENERAL(event, sound1, sound2, sound3,
            current_sound, screen, HEIGHT, MENU_HEIGHT, WIDTH, MENU_WIDTH, menu_type, volume, Finished)

        pygame.display.update()
