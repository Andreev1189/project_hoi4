print("hello VoVa!!!")
from math import *
import pygame
from pygame.draw import *
from random import randint

pygame.init()

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

BORDERS = (1200, 900)
screen = pygame.display.set_mode(BORDERS)

# provinces = [[0, 100, 100], [1, 200, 100], [2, 150, 100 * (1 + 0.5 * sqrt(3))]]
# ways = [[1, 2], [2, 0], [0, 1]]

K = []
Z = []
Provinces = []
Divisions = []
Lines = []



def create_map(el):
    prov = Province(int(el[0]), int(el[1]), 0)
    Provinces.append(prov)

def craeate_lines(el):
    line = Way(int(el[0]), int(el[1]))
    Lines.append(line)

def create_division(current_prov, color):
    div = Division(current_prov, color)
    Divisions.append(div)

def printer(title, text_size=15, base_coords=(10, 10)):
    font = pygame.font.Font(None, text_size)
    text = font.render(str(int(title)), True, [255, 255, 255])
    screen.blit(text, base_coords)


class Timeboss:
    def __init__(self):
        self.TIME = 0
        self.TIMESPEED = 1
        self.time_is_running = -1

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.time_is_running *= -1

    def runtime(self):
        if self.time_is_running == 1:
            self.TIME += self.TIMESPEED

    def speed_changer(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.TIMESPEED = 1
            if event.key == pygame.K_2:
                self.TIMESPEED = 2
            if event.key == pygame.K_3:
                self.TIMESPEED = 3
            if event.key == pygame.K_4:
                self.TIMESPEED = 4
            if event.key == pygame.K_5:
                self.TIMESPEED = 5


timeboss = Timeboss()


class Division:
    def __init__(self, current_prov, color, is_chosen=False, current_way=-1, way_completed=-1, velocity=1, r=10, alive=1):
        self.current_prov = current_prov
        self.color = color
        self.velocity = 1
        self.is_chosen = False
        self.current_way = current_way
        self.way_completed = way_completed
        self.start_moment = -1
        self.r = 10
        self.alive = alive

    def draw(self, Provinces):
        if self.is_chosen == False:
            self.color = default_color
        if self.is_chosen == True:
            self.color = BLUE
        pygame.draw.rect(screen, self.color,
            (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r,
                2 * self.r, self.r))

    def move(self):
        if self.current_way != -1:
            if self.current_way == self.current_prov:
                self.current_prov = self.current_way
                self.current_way = -1
                self.way_completed = -1
                self.is_chosen = False
            else:
                s_now = (timeboss.TIME - self.start_moment) * self.velocity
                s_full = ((Provinces[self.current_prov].x - Provinces[self.current_way].x)**2
                  + (Provinces[self.current_prov].y - Provinces[self.current_way].y)**2) ** (1/2)
                self.way_completed = s_now / s_full
                print(self.way_completed)
                if self.way_completed >= 1:
                    self.current_prov = self.current_way
                    self.current_way = -1
                    self.way_completed = -1
                    self.is_chosen = False

    def battle(self):
        pass

    def chosen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_pos, y_pos = event.pos
                if (x_pos - Provinces[self.current_prov].x) ** 2 + (y_pos - Provinces[self.current_prov].y) ** 2 \
                        <= Provinces[self.current_prov].r ** 2:
                    self.is_chosen = True
                else:
                    self.is_chosen = False

    def direction(self, event, Provinces):
        if self.is_chosen == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    x_pos, y_pos = event.pos
                    for prov in Provinces:
                        if (x_pos - prov.x) ** 2 + (y_pos - prov.y) ** 2 <= prov.r ** 2:
                            self.current_way = Provinces.index(prov)
                            self.way_completed = 0
                            self.start_moment = timeboss.TIME



class Province:
    def __init__(self, x, y, motherland, color=GREEN, r=15):
        self.x = x
        self.y = y
        self.motherland = motherland
        self.color = WHITE
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Way:
    def __init__(self, start_pos, end_pos, color=YELLOW):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color

    def draw(self, Provinces):
        pygame.draw.line(screen, GREY, (Provinces[self.start_pos].x, Provinces[self.start_pos].y),
                                        (Provinces[self.end_pos].x, Provinces[self.end_pos].y), 10)


f1 = open('map.txt', 'r')
f2 = open('ways.txt', 'r')

for line in f1:
    line = line.rstrip()
    K.append(line)


for line in f2:
    line = line.rstrip()
    Z.append(line)


for i, el in enumerate(K):
    el = el.split(' ')
    create_map(el)

for i, el in enumerate(Z):
    el = el.split()
    craeate_lines(el)

default_color = GREEN
create_division(0, default_color)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    EVENTS = pygame.event.get()

    for i, el in enumerate(Lines):
        el.draw(Provinces)

    for i, el in enumerate(Provinces):
        el.draw()


    """
    Kak goJI)I(Ho 6blTb:
    """

    for div in Divisions:
        div.move()
        div.battle()
        for event in EVENTS:
            div.chosen(event)
            div.direction(event, Provinces)
        div.draw(Provinces)

    for event in EVENTS:
        timeboss.check(event)
        timeboss.speed_changer(event)
        if event.type == pygame.QUIT:
            finished = True

    timeboss.runtime()
    printer(timeboss.TIME)

    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
