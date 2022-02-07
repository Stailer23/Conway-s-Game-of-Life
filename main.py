"""
Игра жизни Конвея. Представляет из себя клеточный автомат. Каждая клетка может иметь 2 состояния: мертва или жива.
Клетка умирает, если у нее меньше 2 или больше 3 живых соседей.
Если у мертвой клетки ровно 3 соседа - она становится живой.
В остальных случаях клетки остаются либо мертвыми, либо живыми.
При старте игры создается поле с мертвыми клетками. Игрок нажатием клавиши "1" выбирает какие клетки оживить.
При нажатии клавиши "2" стартует основная логика и клетки меняют свое состояние по перечисленным выше правилам.
При повторном нажатии клавиши "2" игра приостанавливается.
"""

import pygame
import math
import time

window_size_x = 20
window_size_y = 20
cells_size = 36

WIDTH = window_size_x * cells_size + 1
HEIGHT = window_size_y * cells_size + 1
FPS = 30

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
dark_green = (0, 100, 0)
yellow = (255, 255, 0)
pink = (255, 0, 255)

cells = []
life_cell = []
system = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1])
flag = 1

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()


def draw_window():
    """
    Функция рисует игровое поле
    """
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / cells_size) * cells_size
    pos_y = math.floor(mouse_pos[1] / cells_size) * cells_size
    pygame.draw.rect(window, dark_green, [pos_x, pos_y, cells_size, cells_size])
    for Line in range(window_size_x + 1):
        pygame.draw.line(window, green, [Line * cells_size, 0], [Line * cells_size, HEIGHT * cells_size])
    for Line in range(window_size_y + 1):
        pygame.draw.line(window, green, [0, Line * cells_size], [WIDTH, Line * cells_size])


class Cell:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.coord = [int(x // 36), int(y // 36)]

    def draw(self):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.size, self.size])


def create_map_list():
    """
    Функция собирает все созданные клетки в список
    """
    for i in range(window_size_x):
        for j in range(window_size_y):
            if checking_cell_building(i * cells_size, j * cells_size):
                cells.append(Cell(i * cells_size, j * cells_size, 35, black))


def creating_cell():
    """
    Функция создает "живые" клетки при нажатии клавиши "1"
    """
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / cells_size)
    pos_y = math.floor(mouse_pos[1] / cells_size)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        for exmp in cells:
            if exmp.coord == [pos_x, pos_y]:
                exmp.color = green
                life_cell.append(exmp.coord)


def near(pos: list, sys=system):
    """
    Функция поиска соседей.
    """
    count = 0
    for i in sys:
        if [(pos[0] + i[0]) % window_size_x, (pos[1] + i[1]) % window_size_y] in life_cell:
            count += 1
    return count


def logic1():
    """
    Функция удаления клеток, если живых соседей меньше 2 и больше 3.
    """
    for i in range(len(cells)):
        cell = cells[i]

        if near(cell.coord) not in (2, 3) and cell.color == green:
            cell.color = black
            life_cell.remove(cell.coord)


def logic2():
    """
    Функция зарождения клетки, если у нее ровно 3 живых соседа.
    """
    for i in range(len(cells)):

        cell = cells[i]
        if near(cell.coord) == 3 and (cell.color == black):
            cell.color = green
            life_cell.append(cell.coord)


def start():
    """
    Функция мониторит нажатие клавиши "2". При нажатии запускается игра. При повторном нажатии приостанавливается.
    """
    global flag
    keys = pygame.key.get_pressed()
    if keys[pygame.K_2]:
        time.sleep(0.1)
        flag += 1
        return flag


def checking_cell_building(x, y):
    """
    Функция предотвращает создание объектов поверх существующих.
    """
    if len(cells) > 0:
        for cell in cells:
            if cell.x == x and cell.y == y:
                return False
    return True


def Main():
    draw_window()
    create_map_list()
    for cell in cells:
        cell.draw()
    creating_cell()
    start()
    if flag % 2 == 0:
        logic1()
        logic2()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(dark_green)
    Main()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
