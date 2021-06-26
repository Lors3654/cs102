import copy
import pathlib
import random
import typing as tp
from copy import deepcopy
from typing import List, Optional, Tuple

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment

        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                height = cell[0] + i
                widht = cell[1] + j
                if 0 <= widht < self.cols and 0 <= height < self.rows and (i, j) != (0, 0):
                    cells.append(self.curr_generation[height][widht])
        return cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_grid = self.create_grid(False)
        for x in range(self.rows):
            for y in range(self.cols):
                if sum(self.get_neighbours((x, y))) == 3 and (self.curr_generation[x][y] == 0):
                    next_grid[x][y] = 1
                elif (1 < sum(self.get_neighbours((x, y))) < 4) and (
                    self.curr_generation[x][y] == 1
                ):
                    next_grid[x][y] = 1

        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations == self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, "r")
        ln = [[int(col) for col in row.strip()] for row in f]
        f.close()
        game = GameOfLife((len(ln), len(ln[0])))
        game.curr_generation = ln
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        f = open(filename, "w")
        for row in self.curr_generation:
            for coll in row:
                f.write(str(coll))
            f.write("\n")
        f.close()
