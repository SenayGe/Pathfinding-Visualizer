import random
import time
from itertools import zip_longest

import pygame


class Maze:
    def __init__(self, board):
        self.board = board

    def create_outside_wall(self):
        for row in range(self.board.total_rows):
            four_sides = [self.board.grid[row][0],self.board.grid[row][self.board.total_rows-1],
                          self.board.grid[0][row], self.board.grid[self.board.total_rows - 1][row]]

            for node in four_sides:
                if not node.is_start() and not node.is_end():
                    node.make_barrier()

        self.board.draw()

    def maze_recursive_call(self, top, bottom, left, right):
        """
        This is a recursion function that divides the board
        into four section by making barriers. It leaves three
        gaps to serve as passage ways in the maze.
        Barriers/walls fall on even numbered rows while the gaps
        are placed on odd numbered rows. For that reason the
        total number of rows in the board must be odd numbered.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Choose a spot to divide the board horizontally
        start_row_range = bottom + 2
        end_row_range = top - 1
        y = random.randrange(start_row_range, end_row_range, 2)

        # Choose a spot to divide the board vertically
        start_col_range = left + 2
        end_col_range = right - 1
        x = random.randrange(start_col_range, end_col_range, 2)

        # Perform the division
        # for column, row in zip_longest(range(left + 1, right), range(bottom + 1, top)):
        #     if column is not None:
        #         self.board.grid[y][column].make_barrier()  # VERTICAL WAL
        #     if row is not None:
        #         self.board.grid[row][x].make_barrier()  # HORIZONTAL WALL
        #     self.board.draw()
        for column in range(left + 1, right):
            current_node = self.board.grid[y][column]
            if not current_node.is_start() and not current_node.is_end():
                current_node.make_barrier()  # VERTICAL WAL
        for row in range(bottom + 1, top):
            current_node = self.board.grid[row][x]
            if not current_node.is_start() and not current_node.is_end():
                self.board.grid[row][x].make_barrier()  # HORIZONTAL WALL
        self.board.draw()

        # Randomly place passage-way/opening on three of the four walls
        wall = random.randrange(4)
        if wall != 0:
            gap = random.randrange(left + 1, x, 2)  # adding one ensures the opening falls on odd numbered col
            self.board.grid[y][gap].reset()
        if wall != 1:
            gap = random.randrange(x + 1, right, 2)
            self.board.grid[y][gap].reset()
        if wall != 2:
            gap = random.randrange(bottom + 1, y, 2)
            self.board.grid[gap][x].reset()
        if wall != 3:
            gap = random.randrange(y + 1, top, 2)
            self.board.grid[gap][x].reset()
        self.board.draw()

        # if there is enough space on the board for recurssive call

        if top > y + 3 and x > left + 3:
            self.maze_recursive_call(top, y, left, x)

        if top > y + 3 and x + 3 < right:
            self.maze_recursive_call(top, y, x, right)

        if bottom + 3 < y and x + 3 < right:
            self.maze_recursive_call(y, bottom, x, right)

        if bottom + 3 < y and x > left + 3:
            self.maze_recursive_call(y, bottom, left, x)

    def make_maze(self):
        """" creates a maze using recursive division"""
        # First draw outside walls along the edges of the board
        self.create_outside_wall()

        # Perform the recursive process
        self.maze_recursive_call(self.board.total_rows - 1, 0,
                                 0, self.board.total_rows - 1)

