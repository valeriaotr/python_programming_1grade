import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

        # Инициализируем screen
        self._screen = curses.initscr()

    def draw_borders(self) -> None:
        """Отобразить рамку."""
        self._screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self) -> None:
        """Отобразить состояние клеток."""
        # Получаем количество строк и колонок в консольном поле
        num_rows, num_cols = self._screen.getmaxyx()

        # Вычисляем среднюю пазицию по колонке
        middle_col_position = num_cols // 2 - self.life.cell_width
        for row_index, row in enumerate(self.life.current_generation):
            # Вычисляем среднюю позицию по строке
            middle_row_position = num_rows // 2 - self.life.cell_height // 2 + row_index

            # Склеиваем текущую строку матрицы в str тип и заменяем 0 на ' ' и 1 на *
            row_string = " ".join((" " if value else "*" for value in row))
            try:
                self._screen.addstr(middle_row_position, middle_col_position, row_string)
            except curses.error:
                pass

    def run(self) -> None:
        self.draw_borders()
        while True:
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self._screen.refresh()
            self.life.step()

            x = self._screen.getch()
            if x == ord("f"):
                curses.endwin()
                break


if __name__ == "__main__":
    game = GameOfLife(size=(20, 20), randomize=True, max_generations=100)
    console = Console(life=game)
    console.run()
