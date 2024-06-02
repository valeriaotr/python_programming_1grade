from __future__ import annotations

import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
        grid: tp.Optional[Grid] = None,
    ) -> None:
        # Количество ячеек по вертикали и горизонтали
        self.cell_height, self.cell_width = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.current_generation = grid if grid is not None else self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """Создание списка клеток"""
        if not randomize:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]

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
                neighbour_cell = self.current_generation[row_index][col_index]
            except IndexError:
                continue
            else:
                neighbours_list.append(neighbour_cell)

        return neighbours_list

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = [row.copy() for row in self.current_generation]
        for row_index in range(self.cell_height):
            for col_index in range(self.cell_width):
                # Получаем список из соседей каждой клетки и количество живых клеток
                neighbours_list = self.get_neighbours((row_index, col_index))
                alive_neighbours_count = sum(neighbours_list)

                # Если клетка мертва и количество живых соседей == 3, делаем ее живой
                #
                # Если же клетка жива и количество живых соседий от 2 до 3, делаем ее мертвой
                if (not self.current_generation[row_index][col_index]) and (alive_neighbours_count == 3):
                    new_grid[row_index][col_index] = 1
                elif (self.current_generation[row_index][col_index]) and (alive_neighbours_count not in (2, 3)):
                    new_grid[row_index][col_index] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.current_generation = (
            self.current_generation,
            self.get_next_generation(),
        )

        # Инкрементируем количество созданных поколений
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        # Для mypy указываем увереннность, что значение не None
        assert self.max_generations is not None
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.current_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> GameOfLife:
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid_string = filename.read_text()
        grid_list = [[int(value) for value in row] for row in grid_string.split()]

        return GameOfLife(grid=grid_list, size=(len(grid_list), len(grid_list[0])))

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        grid_string = "\n".join("".join(str(value) for value in row) for row in self.current_generation)
        filename.write_text(grid_string)

    def change_curr_generation_grid(self, row_index: int, col_index: int) -> None:
        "Изменяет текущее состояние клеток"
        curr_value = self.current_generation[row_index][col_index]
        self.current_generation[row_index][col_index] = 1 if not curr_value else 0
