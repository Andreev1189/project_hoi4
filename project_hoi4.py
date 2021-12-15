print("hello VoVa!!!")
from math import *
import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 30
TIME = 0
TIMESPEED = 10

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

BORDERS = (1200, 900)
screen = pygame.display.set_mode(BORDERS)

provinces = [[0, 100, 100], [1, 200, 100], [2, 150, 100 * (1 + 0.5 * sqrt(3))]]
ways = [[1, 2], [2, 0], [0, 1]]

K = []
Z = []
Provinces = []
Divisions = []
Lines = []


def create_map(el):

    prov = Province(int(el[0]), int(el[1]), 0)
    print(int(el[0]))
    print(int(el[1]))
    Provinces.append(prov)

def craeate_lines(el):

    line = Way(int(el[0]), int(el[1]))
    Lines.append(line)
    print(int(el[0]))


def create_division(current_prov, color):
    div = Division(current_prov, color)
    Divisions.append(div)

'''
def graf_printer(p, w):
    for np in p:
        circle(screen, (0, 255, 0), (np[1], np[2]), 10, 10)
    for way in w:                                           # He y4uTblBaeT Henop9IgkoBble np.
        polygon(screen, (255, 255, 0), [(p[way[0]][1], p[way[0]][2]), (p[way[1]][1], p[way[1]][2]), 
                                                                (p[way[0]][1], p[way[0]][2])], 5)
'''

def printer(title, text_size=15, base_coords=(10, 10)):
    font = pygame.font.Font(None, text_size)
    text = font.render(str(int(title)), True, [255, 255, 255])
    screen.blit(text, base_coords)


class Division:
    def __init__(self, current_prov, color, chosen=False, current_way=-1, way_completed=-1, velocity=1, r=10, alive=1):
        
        self.current_prov = current_prov
        self.color = color
        self.velocity = 1
        self.chosen = False
        self.current_way = current_way
        self.way_completed = way_completed
        self.r = 10
        self.alive = alive

    def draw(self, Provinces):
        pygame.draw.rect(screen, self.color, 
            (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r,
                2 * self.r, self.r))

    def move(self):
        pass

    def chosen(self, event):
        pass

    def chosen_up(self):
        self.chosen = True

    def chosen_down(self):
        self.chosen = False

class Province:
    def __init__(self, x, y, motherland, color=GREEN, r=15):
        self.x = x
        self.y = y 
        self.motherland = motherland
        self.color = GREEN
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

class Way:
    def __init__(self, start_pos, end_pos, color=YELLOW):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color

    def draw(self, Provinces):
        pygame.draw.line(screen, BLUE, (Provinces[self.start_pos].x, Provinces[self.start_pos].y), 
                                        (Provinces[self.end_pos].x, Provinces[self.end_pos].y), 10)


f1 = open('map.txt', 'r')
f2 = open('ways.txt', 'r')

for line in f1:
    line = line.rstrip()
    K.append(line)

    print(line)
    print(type(line))

for line in f2:
    line = line.rstrip()
    Z.append(line)


for i, el in enumerate(K):
    el = el.split(' ')
    create_map(el)

for i, el in enumerate(Z):
    el = el.split()
    craeate_lines(el)


create_division(0, MAGENTA)


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
    

    for i, el in enumerate(Lines):
        el.draw(Provinces)

    for i, el in enumerate(Provinces):
        el.draw()

    Divisions[0].draw(Provinces)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
