from __future__ import annotations
import random
from functools import cache

__all__ = [
    'Grid', 'max_flow', 'min_flow'
]

max_flow = 1
min_flow = -1

class Grid:
    CellSize = 1
    Width  = 48
    Height = 32
    FluidDensity = 1

    def __init__(self, width: int, height: int, timestep: float) -> None:
        self.width  = width
        self.height = height
        self.timestep = timestep

        self.x_edges = [[random.uniform(min_flow, max_flow) for _ in range(width + 1)] for _ in range(width)]
        self.y_edges = [[random.uniform(min_flow, max_flow) for _ in range(width)] for _ in range(height + 1)]

        self.grid_props = [[(i*4, 0, j*5) for i in range(width)] for j in range(height)]
        self.grid_pressure = [[0.0 for i in range(width)] for j in range(height)]

    def cell_divergence(self, x: int, y: int) -> float:
        v_top = self.y_edges[y][x]
        v_left = self.x_edges[y][x]
        v_right = self.x_edges[y][x+1]
        v_bottom = self.y_edges[y+1][x]

        gradient_x = (v_right - v_left) / Grid.CellSize
        gradient_y = (v_top - v_bottom) / Grid.CellSize

        return gradient_x + gradient_y

    def min_max_pressure(self) -> tuple[float, float]:
        cur_min = 0
        cur_max = 0
        for j in range(self.height):
            for i in range(self.width):
                p = self.get_pressure(i, j)
                if p < cur_min: cur_min = p
                elif p > cur_max: cur_max = p

        return cur_min, cur_max

    def get_pressure(self, x: int, y: int) -> float:
        out_of_bounds = x < 0 or x > self.width-1 or y < 0 or y > self.height-1
        return 0.0 if out_of_bounds else self.grid_pressure[y][x]

    def solve_cell_pressure(self, x: int, y: int) -> None:
        p_top    = self.get_pressure(x, y - 1)
        p_bottom = self.get_pressure(x, y + 1)
        p_left   = self.get_pressure(x - 1, y)
        p_right  = self.get_pressure(x + 1, y)
        v_top    = self.y_edges[y][x]
        v_bottom = self.y_edges[y + 1][x]
        v_left   = self.x_edges[y][x]
        v_right  = self.x_edges[y][x + 1]

        p_sum = p_top + p_bottom + p_left + p_right
        v_sum = v_top + v_bottom + v_left + v_right
        self.grid_pressure[y][x] = (p_sum - Grid.FluidDensity * Grid.CellSize * v_sum / self.timestep) / 4.0

    def solve_pressure(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.solve_cell_pressure(x, y)

    @cache
    def min_and_max_cell_divergence(self) -> tuple[float, float]:
        cur_min = 0
        cur_max = 0
        for j in range(self.height):
            for i in range(self.width):
                d = self.cell_divergence(i, j)
                if d < cur_min: cur_min = d
                elif d > cur_max: cur_max = d

        return cur_min, cur_max
