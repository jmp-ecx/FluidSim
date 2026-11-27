from simulator import *

import pygame as pg

STEPS_PER_SECOND = 5
TIMESTEP = 1 / STEPS_PER_SECOND

WIDTH = 64
HEIGHT = 48

def main() -> None:
    pg.init()

    win = pg.display.set_mode((WIDTH * Grid.CELL_SIZE, HEIGHT * Grid.CELL_SIZE))
    pg.display.set_caption('Fluid Simulator')
    clock = pg.time.Clock()

    grid = Grid(WIDTH, HEIGHT, TIMESTEP)

    db, pb = (0.0, 0.0), (0.0, 0.0)

    has = False
    run = True
    while run:
        _ = clock.tick(STEPS_PER_SECOND) / 1000
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

        if True:
            grid.solve_pressure()
            grid.solve_velocity()

        if not has:
            db = grid.divergence_bounds()
            pb = grid.pressure_bounds()
            has = True

        for y in range(HEIGHT):
            for x in range(WIDTH):
                offset = x*Grid.CELL_SIZE, y*Grid.CELL_SIZE

                # d = grid.divergence(x, y)
                # col = (0,0,0) if d == 0 else (0, 0, min(int(255*d/db[0]), 255)) if d > 0 else (0, min(int(255*d/db[1]), 255), 0)
                # pg.draw.rect(win, col, [*offset, Grid.CELL_SIZE, Grid.CELL_SIZE])

                d = grid.pressure[y][x]
                col = (0,0,0) if d == 0 else (0, 0, min(int(255*d/pb[0]), 255)) if d > 0 else (0, min(int(255*d/pb[1]), 255), 0)
                pg.draw.rect(win, col, [*offset, Grid.CELL_SIZE, Grid.CELL_SIZE])

                if grid.solid_cells[y][x]:
                    pg.draw.rect(win, (255,0,0), [*offset, Grid.CELL_SIZE, Grid.CELL_SIZE])

        pg.display.update()

