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
BLACK = 0x000000
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
all_supplylands = [[0, 1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13]]
logistics_prov = [0, 13]
Divisions = []
Lines = []
battles = []


def create_map(el, motherlands, number):
    prov = Province(int(el[0]), int(el[1]), motherlands, number)
    Provinces.append(prov)

def craeate_lines(el):
    line = Way(int(el[0]), int(el[1]))
    Lines.append(line)

def create_division(current_prov, color, motherland, number, type):
    div = Division(current_prov, color, motherland, number, type)
    Divisions.append(div)


def printer(title, text_size=15, base_coords=(10, 10), color=WHITE):
    font = pygame.font.Font(None, text_size)
    text = font.render(str(int(title)), True, color)
    screen.blit(text, base_coords)


class Timeboss:
    def __init__(self):
        self.TIME = 0
        self.TIMESPEED = 1
        self.time_is_running = -1

    def check(self, event):
        '''
        Проверяет запуск внутриигрового времени
        :param event: нажатие на пробел
        :return: изменяет параметр, отвечающий за ход внутриигрового времени
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.time_is_running *= -1

    def runtime(self):
        '''
        Рассчитывает изменение внутриигрового времени
        :return: изменяет параметр времени
        '''
        if self.time_is_running == 1:
            self.TIME += self.TIMESPEED

    def speed_changer(self, event):
        '''
        Регулировка скорости изменения внутриигрового времени с помощью клавиш 1-5, 0
        :param event: Нажатие клавиш 1-5, 0
        :return: Изменяет параметр скорости
        '''
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

# Создание регулятора времени (только он используетя во время игры)
timeboss = Timeboss()


class Division:
    def __init__(self, current_prov, color,  motherland, number, type, purpose=-1, way_completed=-1, battle_completed=2, r=10, alive=1):
        self.current_prov = current_prov
        self.color = color
        self.is_chosen = False
        self.purpose = purpose
        self.current_way = [-1]
        self.way_completed = way_completed
        self.is_supply = True
        self.start_moment = -1
        self.r = r
        self.alive = alive
        self.motherland = motherland
        self.number = number
        self.type = type
        self.velocity = self.battle_stats()[4]
        self.battle_completed = battle_completed
        self.attack_battle_exist = False
        self.defence_battle_exist = False
        self.attack = self.battle_stats()[0]
        self.defence = self.battle_stats()[2]
        self.base_organisation = self.battle_stats()[1]
        self.organisation = self.base_organisation
        self.supp_factor = self.battle_stats()[3]

    def draw(self, Provinces):
        '''
        Отрисовывает всё, что связано с дивизией -
        её принадлежность, выбранность, текущий путь, организацию, наличие снабжения
        :param Provinces:
        :return:
        '''
        # Блок, отвечающий за принадлежность и выбранность (отображает цвет прямоугольника)
        if self.motherland == 0:
            if not self.is_chosen:
                self.color = default_color
            if self.is_chosen:
                self.color = BLUE
        if self.motherland == 1:
            if not self.is_chosen:
                self.color = RED
            if self.is_chosen:
                self.color = YELLOW
        # Блок, рисующий прямоугольник
        pygame.draw.rect(screen, self.color,
            (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r,
                2 * self.r, self.r))
        # Блок, рисующий организацию
        local_title = self.organisation / self.base_organisation * 100
        local_coords = (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r)
        printer(local_title, text_size=15, base_coords=local_coords, color=BLACK)
        # Блок, рисующий текущий путь
        if self.current_way != [-1] and self.is_chosen == True:
            self.draw_current_way()
        if self.way_completed != -1 and self.is_chosen == True:
            self.draw_current_line()
        self.supply_define()
        # Блок, рисующий наличие снабжения
        if not self.is_supply:
            circle(screen, BLACK,
                   (Provinces[self.current_prov].x - self.r, Provinces[self.current_prov].y - 0.5 * self.r), 3)

    def draw_current_line(self):
        '''
        Функция, рисующая пройденный путь между провинциями
        :return: рисует отрезок
        '''
        R_0 = [Provinces[self.current_prov].x, Provinces[self.current_prov].y]
        R_1 = [Provinces[self.current_way[0]].x, Provinces[self.current_way[0]].y]
        R_line = [R_1[0] - R_0[0], R_1[1] - R_0[1]]
        R_current_line = [self.way_completed * R_line[0], self.way_completed * R_line[1]]
        R_current_dot = [R_0[0] + R_current_line[0], R_0[1] + R_current_line[1]]
        pygame.draw.line(screen, CYAN, R_0, R_1, 3)
        pygame.draw.line(screen, MAGENTA, R_0, R_current_dot, 3)

    def draw_current_way(self):
        '''
        Функция, рисующая предстоящий путь
        :return: рисует ломаную
        '''
        current_way_coords = []
        for el in massive_trans(self.current_way):
            current_way_coords.append([Provinces[el].x, Provinces[el].y])
        total_way_coords = []
        total_way_coords += current_way_coords
        current_way_coords.reverse()
        total_way_coords += current_way_coords
        polygon(screen, CYAN, total_way_coords, 3)

    def move(self):
        '''
        Определяет положение дивизии во времени
        :return: изменяет параметр текущего пути
        '''
        if self.current_way != [-1]:
            # Случай направления на провинцию, в которой дивизия и так стоит
            if self.current_way[0] == self.current_prov:
                self.prov_capture(self.current_way[0])
                self.current_way.pop(0)
                self.way_completed = -1
            # Случай направления на провинцию, соседнюю с данной
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
            # Случай движения по пути-ломаной
            elif len(self.current_way) >= 1:
                s_now = (timeboss.TIME - self.start_moment) * self.velocity
                s_full = ((Provinces[self.current_prov].x - Provinces[self.current_way[0]].x) ** 2
                          + (Provinces[self.current_prov].y - Provinces[self.current_way[0]].y) ** 2) ** (1 / 2)
                self.way_completed = s_now / s_full
                if self.way_completed >= 1:
                    self.prov_capture(self.current_way[0])
                    self.current_prov = self.current_way[0]
                    self.current_way.pop(0)
                    self.attack_battle_check()
                    self.cancel_battle_check()
                    self.start_moment = timeboss.TIME
                    self.way_completed = -1
            # Отмена выбранности дошедшей дивизии
            if len(self.current_way) == 0:
                self.purpose = -1
                self.current_way = [-1]
                self.way_completed = -1
                self.is_chosen = False

    def attack_battle_check(self):
        '''
        Проверка вступления дивизии в бой из-за атаки
        :return: вводит данные о дивизии в класс боя, отмечает дивизию как воюющую
        '''
        # Применяется при переходе в новую провинцию
        for div in Divisions:
            # Случай атаки
            if self.current_way[0] in all_motherlands[-self.motherland-1] and div.motherland != self.motherland and div.current_prov == self.current_way[0]:
                print("battle exist")
                # Проверка на старый бой
                is_battle_exist = False
                for battle in battles:
                    if battle.prov == div.current_prov:
                        battle.attackers.append(self.number)
                        is_battle_exist = True
                        self.attack_battle_exist = True
                # Создание нового боя
                if not is_battle_exist:
                    battles.append(Battle(div.current_prov, attackers=[self.number], defenders=[div.number]))
                    self.attack_battle_exist = True
                    div.defence_battle_exist = True

    def cancel_battle_check(self):
        '''
        Проверка выхода дивизий из боя при перенаправлении
        :return: Выводит дивизии из классов боя, изменяет внутренние параметры, говорящие о наличии боя
        '''
        if self.attack_battle_exist:
            for battle in battles:
                if self.number in battle.attackers:
                    if len(battle.attackers) == 1:
                        for div in Divisions:
                            if div.number in battle.defenders:
                                div.defence_battle_exist = False
                        battles.pop(battles.index(battle))
                    else:
                        battle.attackers.remove(self.number)
            for div in Divisions:
                if div.motherland != self.motherland and div.current_prov == self.current_way[0]:
                    self.attack_battle_check()
                    return False
            self.attack_battle_exist = False

    def prov_capture(self, current_prov):
        '''
        Функция запускается при захвате провинции.
        Функция пересчитывает глобальную переменную, говорящую о снабжаемости провинций.
        Это в тот же момент фиксируется и в других дивизиях
        :param current_prov: Меняющая сторону провинция
        :return: Изменяет all_supplylands
        '''
        if Provinces[current_prov].motherland != self.motherland:
            global all_supplylands
            all_motherlands[Provinces[current_prov].motherland].remove(current_prov)
            all_motherlands[self.motherland].append(current_prov)
            Provinces[current_prov].motherland = self.motherland
            supplylands_0 = supply_account(Lines, all_motherlands[0], logistics_prov)
            supplylands_1 = supply_account(Lines, all_motherlands[1], logistics_prov)
            all_supplylands = [supplylands_0, supplylands_1]
            self.supply_define()

    def supply_define(self):
        '''
        Исходя из пересчёта all_supplylands выясняет снабжаемость
        :return: меняется коэффициент, говорящий о снабжаемости
        '''
        for div in Divisions:
            if div.motherland == 0:
                if div.current_prov in all_supplylands[0]:
                    div.is_supply = True
                else:
                    div.is_supply = False
            if div.motherland == 1:
                if div.current_prov in all_supplylands[1]:
                    div.is_supply = True
                else:
                    div.is_supply = False

    def chosen(self, event):
        '''
        Позволяет выбрать дивизию с помощью клика левой кнопкой мыши
        :param event: клик левой кнопкой мыши по нужной провинции
        :return: изменяет параметр, отвечающий за выбранность
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_pos, y_pos = event.pos
                if (x_pos - Provinces[self.current_prov].x) ** 2 + (y_pos - Provinces[self.current_prov].y) ** 2 \
                        <= Provinces[self.current_prov].r ** 2:
                    self.is_chosen = True
                else:
                    self.is_chosen = False

    def direction(self, event, Provinces):
        '''
        Назначает провинцию, в которую должна придти дивизия.
        Использует алгоритм поиска по графу с ограничением на глубину в 8
        :param event: клик правой кнопкой мыши по нужной провинции
        :param Provinces: все провинции
        :return: Изменяет переменную текущего пути с отсутствия пути на массив предстоящих провинций
        '''
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
                            self.attack_battle_check()
                            self.cancel_battle_check()

    def way_massive(self):
        '''
        Непосредственное использование функции из файла поиска пути
        :return: список предстоящих провинций
        '''
        massive = []
        # Случай выбора текущей провинции:
        if self.purpose == self.current_prov:
            massive.append(self.current_prov)
        # Случай выбора соседней провинции:
        elif self.self_neighbours():
            massive.append(self.purpose)
        # Случай, когда необходимо проводить поиск по графу:
        else:
            massive = final_way(Provinces, Lines, self.current_prov, self.purpose)
        return massive

    def self_neighbours(self):
        '''
        Проверяет, выбрана ли соседняя точка, как цель
        :return: True, если выбранная точка - соседняя
        '''
        for line in Lines:
            if line.start_pos == self.current_prov and line.end_pos == self.purpose:
                return True
            if line.start_pos == self.purpose and line.end_pos == self.current_prov:
                return True

    def battle_stats(self):
        '''
        Считает боевые характеристики, исходя из типа дивизии
        :return: список боевых характеристик
        '''
        org_fix = 2000
        att, base_org, defence, supp_fact, vel = 100, 30, 200, 0.2, 3
        if self.type == 'inf':
            att = 115.1
            base_org = 43.1 * org_fix
            defence = 187.4
            supp_fact = 0.024 * org_fix
            vel = 1
        if self.type == 'moto':
            att = 115.1
            base_org = 43.1 * org_fix
            defence = 187.4
            supp_fact = 0.024 * org_fix
            vel = 3
        if self.type == 'tank':
            att = 545.5
            base_org = 80.8 * org_fix
            defence = 237.2
            supp_fact = 0.028 * org_fix
            vel = 3
        return [att, base_org, defence, supp_fact, vel]

    def calculate_peace_org(self):
        '''
        Отвечает за оснащение дивизии вне боя
        :return: Оснащает дивизию в зоне снабжения, истощает дивизию без снабжения
        '''
        if (not self.defence_battle_exist) and (not self.attack_battle_exist):
            if self.organisation/self.base_organisation < 1:
                if self.is_supply:
                    self.organisation += self.supp_factor
                if not self.is_supply:
                    self.organisation -= self.supp_factor / 10


class Battle:
    def __init__(self, prov, attackers, defenders):
        self.prov = prov
        self.attackers = attackers
        self.defenders = defenders
        self.attack_tanks = self.div_counter()[0]
        self.attack_moto = self.div_counter()[1]
        self.attack_inf = self.div_counter()[2]
        self.defence_tanks = self.div_counter()[3]
        self.defence_moto = self.div_counter()[4]
        self.defence_inf = self.div_counter()[5]

    def calculate_org(self, div_number):
        '''
        Считает показатели в бою для конкретной дивизии-класса
        :param div_number: номер дивизии (обычно self.number)
        :return: ничего не возвращает, изменяет self.параметры внутри класса-дивизии
        '''
        for div in Divisions:
            if div.number == div_number:
                if div_number in self.defenders:
                    div.organisation += - max(0., self.total_attack() * len(self.attack_prov()) ** 1.5 + self.total_defence()) - self.supply_factor(div)
                if div_number in self.attackers:
                    div.organisation += - max(0., self.total_attack() / len(self.attack_prov()) ** 1.5 + self.total_defence()) - self.supply_factor(div)
                if div.organisation < 0:
                    for battle in battles:
                        if div.number in battle.defenders:
                            if len(battle.defenders) == 1:
                                battles.pop(battles.index(battle))
                    Divisions.pop(Divisions.index(div))

    def div_counter(self):
        '''
        Переносит боевые данные дивизий для расчёта боя
        :return: список боевых показателей дивизий
        '''
        attack_tanks = []
        attack_moto = []
        attack_inf = []
        defence_tanks = []
        defence_moto = []
        defence_inf = []
        for div in Divisions:
            if div.type == 'tank' and (div.number in self.attackers):
                attack_tanks.append(div.number)
            if div.type == 'moto' and (div.number in self.attackers):
                attack_moto.append(div.number)
            if div.type == 'inf' and (div.number in self.attackers):
                attack_inf.append(div.number)
            if div.type == 'tank' and (div.number in self.defenders):
                defence_tanks.append(div.number)
            if div.type == 'moto' and (div.number in self.defenders):
                defence_moto.append(div.number)
            if div.type == 'inf' and (div.number in self.defenders):
                defence_inf.append(div.number)
        return [attack_tanks, attack_moto, attack_inf, defence_tanks, defence_moto, defence_inf]

    def total_attack(self):
        '''
        По известной формуле считает коэффициент атаки атакующей стороны в бою
        :return: коэффициент атаки
        '''
        tank_att, moto_att, inf_att = 145.5, 115.1, 115.1
        attack = (len(self.attack_tanks)*tank_att + len(self.attack_moto)*moto_att + len(self.attack_inf)*inf_att) / \
                 (len(self.attack_tanks) + len(self.attack_moto) + len(self.attack_inf))
        return attack

    def total_defence(self):
        '''
        По известной формуле считает коэффициент защиты обороняющейся стороны в бою
        :return: коэффициент защиты
        '''
        tank_defence, moto_defence, inf_defence = 137.2, 187.4, 187.4
        defence = (len(self.defence_tanks)*tank_defence + len(self.defence_moto)*moto_defence + len(self.defence_inf)*inf_defence) / \
                 (len(self.defence_tanks) + len(self.defence_moto) + len(self.defence_inf))
        return defence

    def attack_prov(self):
        '''
        Считает провинции, из которыз производится атака
        :return: список провинций с атакующими дивизиями
        '''
        side_prov = []
        for num in self.attackers:
            for div in Divisions:
                if div.number == num and ((div.current_prov in side_prov) == False):
                    side_prov.append(div.current_prov)
        return side_prov

    def supply_factor(self, div):
        '''
        Считает скорость восполнения огранизации во время боя для формулы
        :param div: рассматриваемая дивизия
        :return: коэффициент скорости снабжения
        '''
        if not div.is_supply:
            return 0
        if div.is_supply:
            return div.supp_factor


class Province:
    def __init__(self, x, y, motherland, number, color=GREEN, r=15):
        self.x = x
        self.y = y
        self.number = number
        self.motherland = motherland
        self.color = WHITE
        self.r = r

    def draw(self):
        '''
        Рисует провинции, их принадлежность
        :return: цветные кружочки на экране
        '''
        if self.motherland == 0:
            self.color = WHITE
        else:
            self.color = GREY
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        if self.number in logistics_prov:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.r, 2)


class Way:
    def __init__(self, start_pos, end_pos, color=YELLOW):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.distance = ((Provinces[start_pos].x - Provinces[end_pos].x)**2 +
                         (Provinces[start_pos].y - Provinces[end_pos].y)**2)**(1/2)

    def draw(self, Provinces):
        '''
        Рисует наличие пути между провинциями
        :param Provinces: Необходим список всех провинций
        :return: линии между провинциями
        '''
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
        create_map(el, 0, i)
    elif i in all_motherlands[1]:
        create_map(el, 1, i)


for i, el in enumerate(Z):
    el = el.split()
    craeate_lines(el)


default_color = GREEN
create_division(0, default_color, 0, number=1, type='inf')
create_division(12, RED, 1, number=-1, type='tank')


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

    for div in Divisions:
        div.move()
        for event in EVENTS:
            div.chosen(event)
            div.direction(event, Provinces)
        div.draw(Provinces)
        if timeboss.time_is_running == 1:
            for i in range(timeboss.TIMESPEED):
                div.calculate_peace_org()
        for battle in battles:
            if div.number in massive_trans(battle.attackers) or div.number in massive_trans(battle.defenders):
                if timeboss.time_is_running == 1:
                    for i in range(timeboss.TIMESPEED):
                        battle.calculate_org(div.number)

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
