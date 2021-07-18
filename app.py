import pygame
from constants import *
from menu import *
from algorithm import Algorithm
from board import Board
from maze import Maze


class App:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False

        # KEYS
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.START_KEY, self.CLEAR_KEY, self.MAZE_KEY = False, False, False
        self.LEFT_MOUSE_CLICK, self.RIGHT_MOUSE_CLICK = False, False

        # DISPLAY
        self.display_w, self.display_h = DISPLAY_W, DISPLAY_H
        self.display = pygame.Surface([self.display_w, self.display_h])
        self.window = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
        pygame.display.set_caption("Pathfinding-Algorithms-Visualizer")
        self.font_name = 'assets/arcade_font.TTF'
        self.search_algorithm = 'A*'  # A* search algo as defaults
        self.main_menu = MainMenu(self)
        self.algorithm_menu = AlgorithmMenu(self)
        self.tutorial_menu = TutorialMenu(self)
        self.menu_screen = MainMenu(self)


    def app_loop(self):
        # while self.playing:
        #     self.check_events()
        #     if self.ESC_KEY:
        #         self.playing = False
        #     self.display.fill(BLACK)
        #     self.draw_text('MENU', 30, WHITE, DISPLAY_W/2, DISPLAY_H/2)
        #     self.window.blit(self.display, (0, 0))
        #     pygame.display.update()
        #     self.reset_keys()
        board = Board(self, ROWS)
        algorithm = Algorithm(board)
        maze = Maze(board)
        start = None
        end = None
        maze_state = OFF
        is_started = False
        path_displayed = False

        while self.playing:
            board.draw()
            self.check_events()

            # -------- USER INTERACTION WITH THE BOARD -----------
            # DRAWING NODES
            if self.LEFT_MOUSE_CLICK:
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_pos(pos)
                node = board.grid[row][col]
                if not start:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif self.RIGHT_MOUSE_CLICK:
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_pos(pos)
                node = board.grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # STARTING PATH FINDING VISUALIZATION
            elif self.START_KEY and start and end:
                # CHECK IF PATH FROM PAST SEARCH IS DISPLAYED
                if path_displayed:
                    for row in board.grid:
                        for node in row:
                            # RESET VISUALIZATION
                            if node.is_closed() or node.is_open() or node.is_path():
                                node.reset()
                            node.update_neighbors(board.grid)
                else:
                    for row in board.grid:
                        for node in row:
                            node.update_neighbors(board.grid)

                algorithm.dijkstra(start, end) if self.search_algorithm == 'Dijkstra' else algorithm.astar(start, end)
                path_displayed = True

            # CLEARING BOARD
            elif self.CLEAR_KEY:
                start = None
                end = None
                board.grid = board.make_grid()

            # RETURNING TO MAIN MENU
            elif self.ESC_KEY:
                self.playing = False

            elif self.MAZE_KEY:
                if start and end:
                    board.clear_barriers()
                maze.make_maze()

            self.blit_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.menu.run_display = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True

                if event.key == pygame.K_UP:
                    self.UP_KEY = True

                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True

                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True

                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True

                if event.key == pygame.K_SPACE:
                    self.START_KEY = True

                if event.key == pygame.K_c:
                    self.CLEAR_KEY = True

                if event.key == pygame.K_m:
                    self.MAZE_KEY = True

            elif pygame.mouse.get_pressed()[0]:
                self.LEFT_MOUSE_CLICK = True

            elif pygame.mouse.get_pressed()[2]:
                self.RIGHT_MOUSE_CLICK = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.START_KEY, self.CLEAR_KEY, self.MAZE_KEY = False, False, False
        self.LEFT_MOUSE_CLICK, self.RIGHT_MOUSE_CLICK = False, False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()




