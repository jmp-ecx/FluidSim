from simulator import *

import pygame as pg

STEPS_PER_SECOND = 5 # TODO - change
TIMESTEP = 1 / STEPS_PER_SECOND

def main() -> None:
    pg.init()

    win = pg.display.set_mode((Grid.Width * Grid.CellSize, Grid.Height * Grid.CellSize))
    pg.display.set_caption('Fluid Simulator')
    clock = pg.time.Clock()

    grid = Grid(Grid.Width, Grid.Height, TIMESTEP, 100)

    has = False
    run = True
    while run:
        _ = clock.tick(STEPS_PER_SECOND) # Gives dt, if needed
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

        if True: # Simulating
            grid.solve_pressure()
            grid.update_velocity()

        if True: # Drawing
            win.fill((0xff, 0xff, 0xff))

            i = 0
            mi, mx = grid.min_and_max_cell_divergence()
            pi, px = grid.min_max_pressure()
            for y in range(Grid.Height):
                for x in range(Grid.Width):
                    offset = x*Grid.CellSize,y*Grid.CellSize

                    # pg.draw.rect(win, grid.grid_props[y][x],
                    #              [*offset, GRID_TILE_SIZE, GRID_TILE_SIZE], 0)

                    d = grid.cell_divergence(x, y)
                    if d == 0:  col = (0, 0, 0)
                    elif d > 0: col = (0, 0, int(255 * (d/mx)))
                    else:       col = (0, int(255 * (d/mi)), 0)

                    # p = grid.grid_pressure[y][x]
                    # if p == 0:  col = (0, 0, 0)
                    # elif p > 0: col = (int(255 * (p/px)), 0, 0)
                    # else:       col = (0, int(255 * (p/pi)), 0)

                    pg.draw.rect(win, col,
                                 [*offset, Grid.CellSize, Grid.CellSize], 0)
                    i += 1
                i += 1

            pg.display.update()

    pg.quit()

def main_() -> None:
    grid = Grid(Grid.Width, Grid.Height, 1/5, 1)

    while True:
        grid.solve_pressure()
        grid.update_velocity()
        g = grid.grid_pressure
        for i in g:
            print(i)
        i = input()
        if i == 'q': break
        print('========')

