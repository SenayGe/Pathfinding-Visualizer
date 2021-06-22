import pygame
import math
from queue import PriorityQueue

WINDOW_WIDTH = 700
WINDOW = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_WIDTH])
pygame.display.set_caption('Pathfinding Algo Visualizer')

BLACK = (0, 20, 20)
BLUE_GREY = (44, 62, 80)
AMBER = (240, 180, 0)
GREEN = (39, 174, 96)
BLUE = (100, 149, 237)
PURPLE = (140, 70, 170)
ORANGE = (220, 65, 10)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = BLUE_GREY
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_visited(self):
        return self.color == GREEN

    def is_queued(self):
        return self.color == BLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = BLUE_GREY

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_visited(self):
        self.color = GREEN

    def make_queued(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = AMBER

    def draw_node(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        # CHECK BELOW
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # CHECK ABOVE
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # CHECK LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

        # CHECK RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])




    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, grid_width):
    grid = []
    node_width = grid_width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_width, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, grid_width):
    node_width = grid_width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * node_width), (grid_width, i * node_width))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (i * node_width, 0), (i * node_width, grid_width))


def draw(win, grid, rows, grid_width):
    win.fill(BLUE_GREY)
    for row in grid:
        for node in row:
            node.draw_node(win)

    draw_grid(win, rows, grid_width)
    pygame.display.update()


def get_clicked_pos(pos, rows, grid_width):
    node_width = grid_width // rows
    y, x = pos

    row = y // node_width
    col = x // node_width

    return row, col


def main(window, width):
    ROWS = 41
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    is_started = False
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if is_started:
                continue

            if pygame.mouse.get_pressed()[0]:  # IF LEFT MOUSE BUTTON IS PRESSED
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[1]:  # IF RIGHT MOUSE BUTTON IS PRESSED
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors()



    pygame.quit()


main(WINDOW, WINDOW_WIDTH)







