print("hello VoVa!!!")
from math import *
import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 30
BORDERS = (1200, 900)
screen = pygame.display.set_mode(BORDERS)

provinces = [[1, 100, 100], [2, 200, 100], [3, 150, 100 * (1 + 0.5 * sqrt(3))]]
ways = [[1, 2], [2, 3], [3, 1]]


# def find_way_to_np:

def graf_printer(p, w):
    for np in p:
        circle(screen, (0, 255, 0), (np[1], np[2]), 10, 10)
    # for way in w:                                           # He y4uTblBaeT Henop9IgkoBble np.
    #     polygon(screen, (255, 255, 0), [(p[way[0]][1], p[way[0]][2]), (p[way[1]][1], p[way[1]][2]), (p[way[0]][1], p[way[0]][2])], 5)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
for way in ways:
    print(provinces[way[0]][1], provinces[way[0]][2], provinces[way[1]][1], provinces[way[1]][2], provinces[way[0]][1],
          provinces[way[0]][2])
while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    graf_printer(provinces, ways)
    pygame.display.update()
    screen.fill((0, 0, 0))



pygame.quit()
