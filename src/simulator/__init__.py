from __future__ import annotations
import random, math

__all__ = [
    'Grid',
]

def clamp(a: float, val: float, b: float) -> float:
    if val < a: return a
    if val > b: return b
    return val
def clamp_i(a: int, val: int, b: int) -> int:
    if val < a: return a
    if val > b: return b
    return val

class Grid:
    CELL_SIZE = 16
    FLUID_DENSITY = 1.0

    def __init__(self, width: int, height: int, timestep: float) -> None:
        self.width = width
        self.height = height
        self.timestep = timestep

        self.v_x = [[random.uniform(-1, 1) for _ in range(width + 1)] for _ in range(height)]
        self.v_y = [[random.uniform(-1, 1) for _ in range(width)] for _ in range(height + 1)]

        self.pressure = [[0.0 for _ in range(width)] for _ in range(height)]

        self.solid_cells = [[0 for _ in range(width)] for _ in range(height)]
        for x in range(width):
            self.solid_cells[0][x] = 1
            self.solid_cells[height-1][x] = 1
        for y in range(height):
            self.solid_cells[y][0] = 1
            self.solid_cells[y][width-1] = 1

        for j in range(height+1):
            for i in range(width):
                self.v_y[j][i] = 0.0
        for j in range(height):
            for i in range(width+1):
                self.v_x[j][i] = 1.0

    def is_solid(self, x: int, y: int) -> int:
        return self.solid_cells[clamp_i(0, y, self.height-1)][clamp_i(0, x, self.width-1)]

    def divergence(self, x: int, y: int) -> float:
        vt = self.v_y[y+0][x]
        vb = self.v_y[y+1][x]
        vl = self.v_x[y][x+0]
        vr = self.v_x[y][x+1]

        dx = (vr - vl) / float(Grid.CELL_SIZE)
        dy = (vt - vb) / float(Grid.CELL_SIZE)

        return dy + dx

    def divergence_bounds(self) -> tuple[float, float]:
        mx = 0.0
        mi = 0.0
        for j in range(self.height):
            for i in range(self.width):
                p = self.divergence(i, j)
                if p < mi: mi = p
                elif p > mx: mx = p
        return mx, mi

    def get_pressure(self, x: int, y: int) -> float:
        out_of_bounds = not ((0 < x < self.width-1) and (0 < y < self.height-1))
        return 0.0 if out_of_bounds else self.pressure[y][x]

    def solve_cell_pressure(self, x: int, y: int) -> None:
        ft = 0.0 if self.is_solid(x, y-1) else 1.0
        fb = 0.0 if self.is_solid(x, y+1) else 1.0
        fl = 0.0 if self.is_solid(x-1, y) else 1.0
        fr = 0.0 if self.is_solid(x+1, y) else 1.0
        flow_edges = ft + fb + fl + fr

        if self.is_solid(x, y) or flow_edges == 0.0:
            self.pressure[y][x] = 0.0
            return

        pt = self.get_pressure(x+0, y-1) * ft
        pb = self.get_pressure(x+0, y+1) * fb
        pl = self.get_pressure(x-1, y+0) * fl
        pr = self.get_pressure(x+1, y+0) * fr

        vt = self.v_y[y+0][x] * ft
        vb = self.v_y[y+1][x] * fb
        vl = self.v_x[y][x+0] * fl
        vr = self.v_x[y][x+1] * fr

        p = pt + pb + pl + pr
        v = vt - vb + vr - vl
        self.pressure[y][x] = (p - Grid.FLUID_DENSITY * Grid.CELL_SIZE * v / self.timestep) / flow_edges

    def solve_pressure(self) -> None:
        for _ in range(10):
            for y in range(self.height):
                for x in range(self.width):
                    self.solve_cell_pressure(x, y)

    def pressure_bounds(self) -> tuple[float, float]:
        mx = 0.0
        mi = 0.0
        for j in range(self.height):
            for i in range(self.width):
                p = self.get_pressure(i, j)
                if p < mi: mi = p
                elif p > mx: mx = p
        return mx, mi

    def solve_velocity(self) -> None:
        k = self.timestep / (Grid.FLUID_DENSITY * Grid.CELL_SIZE)
        for y in range(len(self.v_x)):
            for x in range(len(self.v_x[y])):
                if self.is_solid(x, y) or self.is_solid(x-1, 0):
                    self.v_x[y][x] = 0.0
                    continue

                pl = self.get_pressure(x-1, y)
                pr = self.get_pressure(x, y)
                self.v_x[y][x] -= k * (pr - pl)

        for y in range(len(self.v_y)):
            for x in range(len(self.v_y[y])):
                if self.is_solid(x, y) or self.is_solid(x, y - 1):
                    self.v_y[y][x] = 0.0
                    continue

                pt = self.get_pressure(x, y-1)
                pb = self.get_pressure(x, y)
                self.v_y[y][x] -= k * (pt - pb)
