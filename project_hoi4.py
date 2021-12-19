print("hello VoVa!!!")
from math import *
import pygame
from pygame.draw import *
from random import randint
from way_search import *

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

BORDERS = (700, 700)
screen = pygame.display.set_mode(BORDERS)

# provinces = [[0, 100, 100], [1, 200, 100], [2, 150, 100 * (1 + 0.5 * sqrt(3))]]
# ways = [[1, 2], [2, 0], [0, 1]]

K = []
Z = []
Provinces = []
all_motherlands = [[0, 1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13]]
logistics_prov = [0, 13]
Divisions = []
Lines = []



def create_map(el, motherlands):
    prov = Province(int(el[0]), int(el[1]), motherlands)
    Provinces.append(prov)

def craeate_lines(el):
    line = Way(int(el[0]), int(el[1]))
    Lines.append(line)

def create_division(current_prov, color, motherland):
    div = Division(current_prov, color, motherland)
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
            if event.key == pygame.K_0:
                self.TIMESPEED = 10

timeboss = Timeboss()


class Division:
    def __init__(self, current_prov, color,  motherland, purpose=-1, way_completed=-1, battle_completed=-1, velocity=1, r=10, alive=1):
        self.current_prov = current_prov
        self.color = color
        self.velocity = 3
        self.is_chosen = False
        self.purpose = purpose
        self.current_way = [-1]
        self.way_completed = way_completed
        self.battle_completed = battle_completed
        self.is_supply = True
        self.start_moment = -1
        self.r = 10
        self.alive = alive
        self.motherland = motherland

    def draw(self, Provinces):
        if self.motherland == 0:
            if self.is_chosen == False:
                self.color = default_color
            if self.is_chosen == True:
                self.color = BLUE
        if self.motherland == 1:
            if self.is_chosen == False:
                self.color = RED
            if self.is_chosen == True:
                self.color = YELLOW
        pygame.draw.rect(screen, self.color,
            (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r,
                2 * self.r, self.r))

    def move(self):
        if self.current_way != [-1]:
            if self.current_way[0] == self.current_prov:
                self.prov_capture(self.current_way[0])
                self.current_way.pop(0)
                self.way_completed = -1
            elif len(self.current_way) == 1:
                s_now = (timeboss.TIME - self.start_moment) * self.velocity
                s_full = ((Provinces[self.current_prov].x - Provinces[self.current_way[0]].x)**2
                  + (Provinces[self.current_prov].y - Provinces[self.current_way[0]].y)**2) ** (1/2)
                self.way_completed = s_now / s_full
                if self.way_completed >= 1:
                    self.prov_capture(self.current_way[0])
                    self.current_prov = self.current_way[0]
                    self.purpose = -1
                    self.current_way = [-1]
                    self.way_completed = -1
                    self.is_chosen = False
            elif len(self.current_way) >= 1:
                s_now = (timeboss.TIME - self.start_moment) * self.velocity
                s_full = ((Provinces[self.current_prov].x - Provinces[self.current_way[0]].x) ** 2
                          + (Provinces[self.current_prov].y - Provinces[self.current_way[0]].y) ** 2) ** (1 / 2)
                self.way_completed = s_now / s_full
                if self.way_completed >= 1:
                    self.prov_capture(self.current_way[0])
                    self.current_prov = self.current_way[0]
                    self.current_way.pop(0)
                    self.start_moment = timeboss.TIME
                    self.way_completed = -1
            if len(self.current_way) == 0:
                self.purpose = -1
                self.current_way = [-1]
                self.way_completed = -1
                self.is_chosen = False

    def battle(self):
        pass

    def prov_capture(self, current_prov):
        if Provinces[current_prov].motherland != self.motherland:
            print(current_prov)
            all_motherlands[Provinces[current_prov].motherland].remove(current_prov)
            all_motherlands[self.motherland].append(current_prov)
            Provinces[current_prov].motherland = self.motherland
            supplylands_0 = supply_account(Lines, all_motherlands[0], logistics_prov)
            supplylands_1 = supply_account(Lines, all_motherlands[1], logistics_prov)
            print("supplylands", supplylands_0, supplylands_1)
            print("motherlands", all_motherlands[self.motherland], all_motherlands[-1-self.motherland])

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
                            self.purpose = Provinces.index(prov)
                            self.current_way = self.way_massive()
                            self.way_completed = 0
                            self.start_moment = timeboss.TIME

    def way_massive(self):
        massive = []
        # TpuBuaJIbHblu cJIy4au:
        if self.purpose == self.current_prov:
            massive.append(self.current_prov)
        # CJIy4au cocegeu:
        elif self.self_neighbours():
            massive.append(self.purpose)
        # CJIy4au He cocegeu:
        else:
            massive = final_way(Provinces, Lines, self.current_prov, self.purpose)
        return massive

    def self_neighbours(self):
        for line in Lines:
            if line.start_pos == self.current_prov and line.end_pos == self.purpose:
                return True
            if line.start_pos == self.purpose and line.end_pos == self.current_prov:
                return True



class Province:
    def __init__(self, x, y, motherland=0, color=GREEN, r=15):
        self.x = x
        self.y = y
        self.motherland = motherland
        self.color = WHITE
        self.r = r

    def draw(self):
        if self.motherland == 0:
            self.color = WHITE
        else:
            self.color = GREY
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)



class Way:
    def __init__(self, start_pos, end_pos, color=YELLOW):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.distance = ((Provinces[start_pos].x - Provinces[end_pos].x)**2 +
                         (Provinces[start_pos].y - Provinces[end_pos].y)**2)**(1/2)

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
    if i in all_motherlands[0]:
        create_map(el, 0)
    elif i in all_motherlands[1]:
        create_map(el, 1)


for i, el in enumerate(Z):
    el = el.split()
    craeate_lines(el)

default_color = GREEN
create_division(0, default_color, 0)
create_division(12, RED, 1)



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
    screen.fill((0, 0, 40))

pygame.quit()
