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

    def __init__(self, width: int, height: int) -> None:
        self.width  = width
        self.height = height

        self.x_edges = [[random.uniform(min_flow, max_flow) for _ in range(width + 1)] for _ in range(width)]
        self.y_edges = [[random.uniform(min_flow, max_flow) for _ in range(width)] for _ in range(height + 1)]

        self.grid_props = [[(i*4, 0, j*5) for i in range(width)] for j in range(height)]
        self.grid_pressure = [[0 for i in range(width)] for j in range(height)]

    def cell_divergence(self, x: int, y: int) -> float:
        v_top = self.y_edges[y][x]
        v_left = self.x_edges[y][x]
        v_right = self.x_edges[y][x+1]
        v_bottom = self.y_edges[y+1][x]

        gradient_x = (v_right - v_left) / Grid.CellSize
        gradient_y = (v_top - v_bottom) / Grid.CellSize

        return gradient_x + gradient_y

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
