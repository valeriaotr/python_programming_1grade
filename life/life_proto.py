import random
import typing as tp

import pygame
from pygame import QUIT

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    grid: Grid

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Цвета, в которые могут окрашиваться клетки
        self._rect_colors = {
            "alive_color": pygame.Color("green"),
            "dead_color": pygame.Color("white"),
        }

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """Создание списка клеток"""
        if not randomize:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row_index in range(self.cell_height):
            for col_index in range(self.cell_width):
                rect_value = self.grid[row_index][col_index]
                color = self._rect_colors["dead_color"] if not rect_value else self._rect_colors["alive_color"]

                pygame.draw.rect(
                    surface=self.screen,
                    color=color,
                    rect=(col_index, row_index, self.cell_size, self.cell_size),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Получение списка соседних клеток.
        """
        row_position, col_position = cell

        # Все возможные соседние позиции
        neighbours_positions_tuple = (
            (row_position, col_position - 1),
            (row_position - 1, col_position),
            (row_position, col_position + 1),
            (row_position + 1, col_position),
            (row_position - 1, col_position - 1),
            (row_position - 1, col_position + 1),
            (row_position + 1, col_position - 1),
            (row_position + 1, col_position + 1),
        )

        neighbours_list = []
        for row_index, col_index in neighbours_positions_tuple:
            # Если координаты позиции отрицательные => такой позиции не существует
            if row_index < 0 or col_index < 0:
                continue

            try:
                neighbour_cell = self.grid[row_index][col_index]
            except IndexError:
                continue
            else:
                neighbours_list.append(neighbour_cell)

        return neighbours_list

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = [row.copy() for row in self.grid]
        for row_index in range(self.cell_height):
            for col_index in range(self.cell_width):
                # Получаем список из соседей каждой клетки и количество живых клеток
                neighbours_list = self.get_neighbours((row_index, col_index))
                alive_neighbours_count = sum(neighbours_list)

                # Если клетка мертва и количество живых соседей == 3, делаем ее живой
                # Если же клетка жива и количество живых соседий от 2 до 3, делаем ее мертвой
                if (not self.grid[row_index][col_index]) and (alive_neighbours_count == 3):
                    new_grid[row_index][col_index] = 1
                elif (self.grid[row_index][col_index]) and (alive_neighbours_count not in (2, 3)):
                    new_grid[row_index][col_index] = 0

        return new_grid
