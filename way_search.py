import pygame
from pygame.draw import *
from random import randint

# Данные параметры необходимы для ограничения поиска во времени
way_DIAMETR = 8 + 2
supply_DIAMETR = 2 + 2

def check_elem_in_list(l, el):
    '''
    Проверяет, находится ли целый элемент в многомерном списке
    :param l: многомерный список
    :param el: целый элемент
    :return: True, если элемент есть, False, если элемента нет
    '''
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
    '''
    Находит список провинций, соседних данной
    :param Lines: список связей рассматриваемого графа
    :param self_current_prov: интересуемая провинция
    :return: список соседних провинций
    '''
    massive = []
    for line_1 in Lines:
        if self_current_prov == line_1.start_pos:
            massive.append(line_1.end_pos)
        elif self_current_prov == line_1.end_pos:
            massive.append(line_1.start_pos)
    return massive

def self_neibours_for_GRAPH(Lines, self_current_prov):
    '''
    Находит список провинций, соседних данной, в удобной для конкретного случая форме
    :param Lines: список связей рассматриваемого графа
    :param self_current_prov: интересуемая провинция
    :return: список соседних провинций, оформленных в []
    '''
    massive = []
    for line_1 in Lines:
        if self_current_prov == line_1.start_pos:
            massive.append([line_1.end_pos])
        elif self_current_prov == line_1.end_pos:
            massive.append([line_1.start_pos])
    return massive

# Классы переменных нужны следующей функции
list_class = type([1])
int_class = type(1)
def massive_trans(massive):
    '''
    Переводит многомерный список целых переменных в одномерный список тех же переменных в том же порядке
    :param massive: многомерный список
    :return: одномерный список
    '''
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
    '''
    Поиск в ширину по произвольному графу.
    Работает до тех пор, пока не найдёт нужную вершину.
    Компьютер не выдерживает на глубине поиска, большей 10
    :param Lines: Список связей в произвольном графе
    :param self_current_prov: провинция, откуда идёт поиск
    :param self_purpose: искомая провинция
    :param DIAMETR: глубина поиска
    :return: Многомерный массив всех путей данной глубины, если искомое находится. Специальный массив, если не нашлось
    '''
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
    '''
    Превращает список с повторяющимися подряд элементами в список без повторений
    :param numbers: входной список
    :return: список без повторений
    '''
    list_of_unique_numbers = []
    for number in numbers:
        if not (number in list_of_unique_numbers):
            list_of_unique_numbers.append(number)

    return list_of_unique_numbers

def antifirst_prov(GRAPH_1, GRAPH_2, self_purpose):
    '''
    Функция создана для того, чтобы из супермассива всех возможных путей данной глубины
    выбирать массивы чисел двух соседних глубин и находить те провинции из меньшей глубины,
    из которых можно попасть в требуемые на большей глубине
    :param GRAPH_1: Массив чисел большей глубины (-1)
    :param GRAPH_2: Массив чисел меньшей глубины (-2)
    :param self_purpose: провинция от GRAPH_1, в которую нужно попасть из GRAPH_2
    :return: список провинций, из которых можно попасть в данную
    '''
    provinces = []
    for i in range(0, len(GRAPH_1)):
        for j in range(0, len(GRAPH_1[i])):
            if GRAPH_1[i][j] == self_purpose:
                provinces.append(massive_trans(GRAPH_2)[i])
    return get_unique_numbers(provinces)

def way_distance(Provinces, massive):
    '''
    Считает длину пути по провинциям из списка
    :param Provinces: наши провинции
    :param massive: упорядоченный список провинций в маршруте
    :return: длину пути (в пикселях)
    '''
    dist = 0
    for i in range(0, len(massive)-1):
        dist += ((Provinces[massive[i]].x - Provinces[massive[i+1]].x) ** 2 +
         (Provinces[massive[i]].y - Provinces[massive[i+1]].y) ** 2) ** (1 / 2)
    return dist

def min_dist_finder(Provinces, deep_GRAPH):
    '''
    Работает с графом возможных путей из точки до точки
    Сверяет путь только что удалённого пути с "нулевым" путём графа
    Цикл повторяется, пока граф не удалится
    Тем самым все пути перебираются
    :param Provinces: провинции
    :param deep_GRAPH: упорядоченный граф возможных путей
    :return: минимальный по длине путь как массив провинций
    '''
    current_way = zero_way(deep_GRAPH)
    deep_GRAPH = delete_zero_way(deep_GRAPH)
    for i in range(len(massive_trans(deep_GRAPH[1]))-1):
        if min(way_distance(Provinces, current_way), way_distance(Provinces, zero_way(deep_GRAPH))) == way_distance(Provinces, zero_way(deep_GRAPH)):
            current_way = zero_way(deep_GRAPH)
        deep_GRAPH = delete_zero_way(deep_GRAPH)
    return current_way

def zero_way(deep_GRAPH):
    '''
    Вспомогательная функция для работы с графом путей от точки до точки
    Находит "нулевой" путь - входящий в граф с нулевыми индексами
    :param deep_GRAPH: граф путей от точки до точки
    :return: "нулевой" путь
    '''
    zero_way = []
    for p in range(len(deep_GRAPH)):
        zero_way.append(deep_GRAPH[p][0][0])
    return zero_way

def delete_zero_way(deep_GRAPH):
    '''
    Удаляет из графа "нулевой" путь
    :param deep_GRAPH: граф путей от точки до точки
    :return: тот же граф, но без "нулевого" пути
    '''
    for i in range(1, len(deep_GRAPH)-1):
        if len(deep_GRAPH[i][0]) > 1:
            deep_GRAPH[i][0].pop(0)
            break
        elif len(deep_GRAPH[i][0]) == 1:
            deep_GRAPH[i].pop(0)

    return deep_GRAPH

def final_way(Provinces, Lines, self_current_prov, self_purpose):
    '''
    Из графа всех путей данной глубины создаёт граф путей от данной точки до данной точки
    Из этого графа находится минимальный путь
    Учитывает вырожденные случаи
    Данная функция используется в классе дивизий
    :param Provinces: список провинций (мб произвольный)
    :param Lines: список наличия путей (мб произвольный)
    :param self_current_prov: провинция, откуда производится поиск
    :param self_purpose: провинция, до которой надо найти путь
    :return: упорядоченный список провинций в наилушем пути
    '''
    a = find_distance(Lines, self_current_prov, self_purpose)
    # отсутствие приемлемого пути:
    if a == [-1, -1, -1]:
        return [self_current_prov]
    deep = a[0]
    count = a[1]
    GRAPH = a[2]
    current_deep = 1
    deep_prov = antifirst_prov(GRAPH[-1], GRAPH[-2], self_purpose)
    deep_GRAPH = [[[self_purpose]], [antifirst_prov(GRAPH[-1], GRAPH[-2], self_purpose)]]
    while not current_deep == deep - 1:
        current_deep_prov = []
        for prov in massive_trans(deep_prov):
            current_deep_prov.append(
                antifirst_prov(GRAPH[-current_deep - 1], GRAPH[-current_deep - 2], prov))  # PEKYPCU9I!!!!!!!
        deep_GRAPH.append(current_deep_prov)
        deep_prov = massive_trans(current_deep_prov)
        deep_GRAPH.append(current_deep_prov)
        current_deep += 1
    deep_GRAPH.append(GRAPH[0])
    deep_GRAPH.reverse()
    deep_GRAPH = get_unique_numbers(deep_GRAPH)
    way_massive = min_dist_finder(Provinces, deep_GRAPH)
    return way_massive


# Механика снабжения:

def true_logistics_prov(motherlands, logistics_prov):
    '''
    Функция находит дружественные центры снабжения на карте
    :param motherlands: свои провинции
    :param logistics_prov: все центры снабжения
    :return: свои центры снабжения
    '''
    true_log_prov = []
    for prov in logistics_prov:
        if prov in motherlands:
            true_log_prov.append(prov)
    return true_log_prov

def true_Lines(Lines, motherlands):
    '''
    Функция ищет наличие путей между дружественными провинциями
    :param Lines: все пути между провинциями
    :param motherlands: свои провинции
    :return: только те lines, которые связывают свои провинции
    '''
    true_lines = []
    for way in Lines:
        if (way.start_pos in motherlands) and (way.end_pos in motherlands):
            true_lines.append(way)
    return true_lines

def supply_account(Lines, motherlands, logistics_prov):
    '''
    Функция подсчитывает те дружественные провинции, которые снабжаются от центров снабжения
    :param Lines: все провинции
    :param motherlands: свои провинции
    :param logistics_prov: все центры снабжения
    :return: свои снабжаемые провинции
    '''
    supplylands = []
    true_log_prov = true_logistics_prov(motherlands, logistics_prov)
    supplylands.append(true_log_prov)
    true_lines = true_Lines(Lines, motherlands)
    for log_prov in true_log_prov:
        for prov in motherlands:
            if find_distance(true_lines, log_prov, prov, DIAMETR=supply_DIAMETR) != [-1, -1, -1]:
                supplylands.append(prov)
    return supplylands

