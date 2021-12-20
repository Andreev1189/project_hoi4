import pygame
from pygame.draw import *
from random import randint

way_DIAMETR = 8 + 2
supply_DIAMETR = 2 + 2

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

def find_distance(Lines, self_current_prov, self_purpose, DIAMETR=way_DIAMETR):
    deep = 1
    count = 0
    iteration_prov = self_neibours(Lines, self_current_prov)
    GRAPH = [[[self_current_prov]], self_neibours_for_GRAPH(Lines, self_current_prov)]
    while not check_elem_in_list(iteration_prov, self_purpose):
        current_iteration_prov = []
        for prov in iteration_prov:
            current_iteration_prov.append(self_neibours(Lines, prov))
        count = massive_trans(current_iteration_prov).count(self_purpose)
        GRAPH.append(current_iteration_prov)
        iteration_prov = massive_trans(current_iteration_prov)
        deep += 1
        if len(GRAPH) == DIAMETR:
            deep = -1
            count = -1
            GRAPH = -1
            break
    return [deep, count, GRAPH]

def get_unique_numbers(numbers):
    list_of_unique_numbers = []
    for number in numbers:
        if not (number in list_of_unique_numbers):
            list_of_unique_numbers.append(number)

    return list_of_unique_numbers

def antifirst_prov(GRAPH_1, GRAPH_2, self_purpose):
    provinces = []
    for i in range(0, len(GRAPH_1)):
        for j in range(0, len(GRAPH_1[i])):
            if GRAPH_1[i][j] == self_purpose:
                provinces.append(massive_trans(GRAPH_2)[i])
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
    if a == [-1, -1, -1]:
        return [self_current_prov]
    deep = a[0]
    count = a[1]
    GRAPH = a[2]
    current_deep = 1
    deep_prov = antifirst_prov(GRAPH[-1], GRAPH[-2], self_purpose)
    deep_GRAPH = [[[self_purpose]], [antifirst_prov(GRAPH[-1], GRAPH[-2], self_purpose)]]
    while not current_deep == deep-1:
        current_deep_prov = []
        for prov in massive_trans(deep_prov):
            current_deep_prov.append(antifirst_prov(GRAPH[-current_deep-1], GRAPH[-current_deep-2], prov))           # PEKYPCU9I!!!!!!!
        deep_GRAPH.append(current_deep_prov)
        deep_prov = massive_trans(current_deep_prov)
        deep_GRAPH.append(current_deep_prov)
        current_deep += 1
    deep_GRAPH.append(GRAPH[0])
    deep_GRAPH.reverse()
    deep_GRAPH = get_unique_numbers(deep_GRAPH)
    # for i in range(0, len(deep_GRAPH)):
    #     deep_GRAPH[i] = get_unique_numbers(deep_GRAPH[i])
    # print(deep_GRAPH)
    min_i = 5000
    min_j = 5000
    min_dist = 10000
    first_way = []
    for p in range(len(deep_GRAPH)):
        first_way.append(deep_GRAPH[p][0][0])
        # deep_GRAPH[p][0].pop(0)
    print("first_way", first_way)
    for i in range(len(deep_GRAPH)):
        for j in range(len(deep_GRAPH[i])):
            pass
    way_massive = first_way
    return way_massive


# MexaHuka cHa6)I(eHu9I:

# ПОЛУЧАЕТ свои провинции, все центры снабжения, ВЫДАЁТ свои центры снабжения
def true_logistics_prov(motherlands, logistics_prov):
    true_log_prov = []
    for prov in logistics_prov:
        if prov in motherlands:
            true_log_prov.append(prov)
    return true_log_prov

# ПОЛУЧАЕТ свои провинции, все Lines, ВЫДАЁТ только те lines, которые связывают свои провинции
def true_Lines(Lines, motherlands):
    true_lines = []
    for way in Lines:
        if (way.start_pos in motherlands) and (way.end_pos in motherlands):
            way.color = 0xFFC91F
            true_lines.append(way)
    return true_lines

# ПОЛУЧАЕТ свои провинции, все центры снабжения, ВЫДАЁТ снабжаемые провинции
def supply_account(Lines, motherlands, logistics_prov):
    supplylands = []
    true_log_prov = true_logistics_prov(motherlands, logistics_prov)
    true_lines = true_Lines(Lines, motherlands)
    for log_prov in true_log_prov:
        for prov in motherlands:
            if find_distance(true_lines, log_prov, prov, DIAMETR=supply_DIAMETR) != [-1, -1, -1]:
                supplylands.append(prov)
    return supplylands
