print("hello VoVa!!!")
from math import *
import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 30
TIME = 0
TIMESPEED = 10

BORDERS = (1200, 900)
screen = pygame.display.set_mode(BORDERS)

provinces = [[0, 100, 100], [1, 200, 100], [2, 150, 100 * (1 + 0.5 * sqrt(3))]]
ways = [[1, 2], [2, 0], [0, 1]]



def create_map():
    prov = Province()
    Provinces.append(prov)


def graf_printer(p, w):
    for np in p:
        circle(screen, (0, 255, 0), (np[1], np[2]), 10, 10)
    for way in w:                                           # He y4uTblBaeT Henop9IgkoBble np.
        polygon(screen, (255, 255, 0), [(p[way[0]][1], p[way[0]][2]), (p[way[1]][1], p[way[1]][2]), 
                                                                (p[way[0]][1], p[way[0]][2])], 5)

class Division:
    def __init__(self, current_prov, chosen=False, velocity = 1, r = 10, alive = 0):
        self.number = number
        self.current_prov = number
        self.velocity = 1
        self.chosen = False
        self.r = 10

    def move(self):
        pass

    def draw(self):
        pass

    def chosen(self, event):
        pass




class Province:
    def __init__(self, x, y, motherland):
        self.x = x
        self.y = y 
        self.motherland = motherland




def printer(title, text_size=15, base_coords=(10, 10)):
    font = pygame.font.Font(None, text_size)
    text = font.render(str(int(title)), True, [255, 255, 255])
    screen.blit(text, base_coords)

# def timeboss(t, ts):
#     t += ts
#     for event in pygame.event.get():
#         if event.type == pygame.K_SPACE:
#             ts += 1
#             ts = ts % 6

def timeboss(t):
    t += TIMESPEED
    return t

pygame.display.update()
clock = pygame.time.Clock()
finished = False


while not finished:
    clock.tick(FPS)

    TIME = timeboss(TIME)
    printer(TIME)
    print(TIME)

    ()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


    graf_printer(provinces, ways)
    pygame.display.update()
    screen.fill((0, 0, 0))



pygame.quit()
