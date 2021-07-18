import pygame
from constants import *



class Node:
    def __init__(self, row, col, board):
        pygame.init()
        self.board = board
        self.row = row
        self.col = col
        self.total_rows = self.board.total_rows
        self.width = self.board.grid_width // self.board.total_rows
        self.y = row * self.width
        self.x = col * self.width
        self.color = BLUE_GREY
        self.neighbors = []

        # self.grid = self.board.grid

    def get_pos(self):
        return self.row, self.col

    def is_open(self):
        return self.color == AQUA

    def is_closed(self):
        return self.color == TURQUOISE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def is_path(self):
        return self.color == AMBER

    def reset(self):
        self.color = BLUE_GREY

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_closed(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = AQUA

    def make_barrier(self):
        self.color = BLACK

    def make_neighbor(self):
        self.color = AMBER

    def make_path(self):
        self.color = AMBER

    def draw_node(self, window, circle=False):
        if circle:
            pygame.draw.circle(window, self.color, ((self.x + self.width//2), (self.y + self.width//2)), self.width//3)

        else:
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
