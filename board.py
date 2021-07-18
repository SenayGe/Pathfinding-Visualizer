import pygame
from constants import *
from node import Node
import time


class Board:
    def __init__(self, app, total_rows):
        self.app = app
        self.grid_width = self.app.display_h
        # self.grid_height = self.grid_width
        self.total_rows = total_rows
        self.grid = self.make_grid()
        self.start_node = None
        self.end_node = None

    def make_grid(self):
        grid = []
        for row in range(self.total_rows):
            grid.append([])
            for col in range(self.total_rows):
                node = Node(row, col, self)
                grid[row].append(node)
        return grid

    def draw_grid(self):
        node_width = self.grid_width // self.total_rows
        for i in range(self.total_rows):
            # DRAWING HORIZONTAL LINES
            pygame.draw.line(self.app.display, BLACK, (i * node_width, 0), (i * node_width, self.grid_width))
            for j in range(self.total_rows):
                # DRAWING VERTICAL LINES
                pygame.draw.line(self.app.display, BLACK, (0, i * node_width), (self.grid_width, i * node_width))

    def draw(self):
        self.app.display.fill(BLUE_GREY)
        for row in self.grid:
            for node in row:
                if node.is_open():
                    # pygame.draw.rect(win, GREEN2, (node.x, node.y, node.width, node.width))
                    node.draw_node(self.app.display, circle=True)
                else:
                    node.draw_node(self.app.display)

        self.draw_grid()
        self.app.window.blit(self.app.display, (0, 0))
        pygame.display.update()

    def clear_barriers(self):
        for row in self.grid:
            for node in row:
                if node.is_barrier() or node.is_open() or node.is_closed() or node.is_path():
                    node.reset()

    def get_clicked_pos(self, pos):
        node_width = self.grid_width // self.total_rows
        x, y = pos

        row = y // node_width
        col = x // node_width

        return row, col

    def show_path(self, current, start, came_from):
        while came_from[current] != start:
            current = came_from[current]
            current.make_path()
            self.draw()
            time.sleep(0.00001)
