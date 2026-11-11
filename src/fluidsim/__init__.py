from simulator import *

import pygame as pg

GRID_TILE_SIZE = 24
STEPS_PER_SECOND = 5 # TODO - change

def main() -> None:
    pg.init()

    win = pg.display.set_mode((Grid.Width * GRID_TILE_SIZE, Grid.Height * GRID_TILE_SIZE))
    pg.display.set_caption('Fluid Simulator')
    clock = pg.time.Clock()

    grid = Grid(Grid.Width, Grid.Height)

    run = True
    while run:
        _ = clock.tick(STEPS_PER_SECOND) # Gives dt, if needed
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

        if True: # Simulating
            ...

        if True: # Drawing
            win.fill((0xff, 0xff, 0xff))

            i = 0
            mi, mx = grid.min_and_max_cell_divergence()
            for y in range(Grid.Height):
                for x in range(Grid.Width):
                    offset = x*GRID_TILE_SIZE,y*GRID_TILE_SIZE

                    # pg.draw.rect(win, grid.grid_props[y][x],
                    #              [*offset, GRID_TILE_SIZE, GRID_TILE_SIZE], 0)

                    d = grid.cell_divergence(x, y)

                    if d == 0:  col = (0, 0, 0)
                    elif d > 0: col = (0, 0, int(255 * (d/mx)))
                    else:       col = (0, int(255 * (d/mi)), 0)

                    pg.draw.rect(win, col,
                                 [*offset, GRID_TILE_SIZE, GRID_TILE_SIZE], 0)
                    i += 1
                i += 1

            pg.display.update()

    pg.quit()
