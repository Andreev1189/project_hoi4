import pygame
from pygame.draw import *
from random import randint

l = [1, [2, 3], [4, [5, 6, [7, [8]]]], [9, 10]]
def check_elem_in_list(l, el):
    if isinstance(l, int):
        if l == el:
            return True
        else:
            return False
    for i in l:
        if isinstance(i, int):
            if i == el:
                return True
        else:
            r = check_elem_in_list(i, el)
            if r:
                return True
    return False

def self_neibours(Lines, self_current_prov):
    massive = []
    for line_1 in Lines:
        if self_current_prov == line_1.start_pos:
            massive.append(line_1.end_pos)
        elif self_current_prov == line_1.end_pos:
            massive.append(line_1.start_pos)
    return massive

def self_neibours_for_GRAPH(Lines, self_current_prov):
    massive = []
    for line_1 in Lines:
        if self_current_prov == line_1.start_pos:
            massive.append([line_1.end_pos])
        elif self_current_prov == line_1.end_pos:
            massive.append([line_1.start_pos])
    return massive

list_class = type([1])
int_class = type(1)
def massive_trans(massive):
    new_massive = []
    local_big_flag = False
    while local_big_flag == False:
        for el in massive:
            if type(el) == int_class:
                new_massive.append(el)
            if type(el) == list_class:
                new_massive += el
        local_flag = True
        for el in massive:
            if type(el) == list_class:
                local_flag = False
        if local_flag == True:
            local_big_flag = True
            return new_massive
        massive = new_massive
        new_massive = []

def find_distance(Lines, self_current_prov, self_purpose):
    deep = 1
    count = 0
    iteration_prov = self_neibours(Lines, self_current_prov)
    GRAPH = [[[self_current_prov]], self_neibours_for_GRAPH(Lines, self_current_prov)]
    while not check_elem_in_list(iteration_prov, self_purpose):
        current_iteration_prov = []
        for prov in iteration_prov:
            current_iteration_prov.append(self_neibours(Lines, prov))
        # print(current_iteration_prov)
        count = iteration_prov.count(self_purpose)
        GRAPH.append(current_iteration_prov)
        iteration_prov = massive_trans(current_iteration_prov)
        deep += 1
    print([deep, count, GRAPH])
    return [deep, count, GRAPH]

def get_unique_numbers(numbers):
    list_of_unique_numbers = []
    for number in numbers:
        if not (number in list_of_unique_numbers):
            list_of_unique_numbers.append(number)
    return list_of_unique_numbers

def antifirst_prov(GRAPH, self_purpose):
    provinces = []
    for i in range(len(GRAPH[-1])):
        for j in range(len(GRAPH[-1][i])):
            if j == self_purpose:
                provinces.append(massive_trans(GRAPH[-2][i]))
    print(provinces)
    return get_unique_numbers(provinces)

def way_distance(Provinces, massive):
    dist = 0
    for n in range(0, len(massive)-2):
        dist += ((Provinces[n].x - Provinces[n+1].x) ** 2 +
         (Provinces[n].y - Provinces[n+1].y) ** 2) ** (1 / 2)
    return dist

def final_way(Provinces, Lines, self_current_prov, self_purpose):
    way_massive = []
    a = find_distance(Lines, self_current_prov, self_purpose)
    deep = a[0]
    count = a[1]
    GRAPH = a[2]
    # prov_one_deep = antifirst_prov(GRAPH, self_purpose)
    current_deep = 1
    # current_count = 0
    deep_prov = antifirst_prov(GRAPH, self_purpose)
    deep_GRAPH = [[[self_purpose]], [antifirst_prov(GRAPH, self_purpose)]]
    while not current_deep == deep:
        current_deep_prov = []
        for prov in deep_prov:
            current_deep_prov.append(antifirst_prov(GRAPH, prov))
        deep_GRAPH.append(current_deep_prov)
        deep_prov = massive_trans(current_deep_prov)
        deep_GRAPH.append(current_deep_prov)
        current_deep += 1
    min_i = 5000
    min_j = 5000
    min_dist = 10000
    first_way = []
    for p in range(0, deep-1):
        first_way.append(deep_GRAPH[p][0][0])
        # deep_GRAPH[p][0].pop(0)
    for i in range(len(deep_GRAPH)):
        for j in range(len(deep_GRAPH[i])):
            pass
    way_massive = first_way
    return way_massive



