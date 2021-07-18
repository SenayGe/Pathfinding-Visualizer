import pygame
from constants import *


class Menu:
    def __init__(self, app):
        self.app = app
        self.mid_w, self.mid_h = app.display_w/2, app.display_h/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 30, 30)
        self.offset = -165  # CURSOR POSITION OFFSET
        img = pygame.image.load('assets/background_img2.PNG')
        self.background = pygame.transform.smoothscale(img, (DISPLAY_W, DISPLAY_H))

    def draw_cursor(self):
        self.app.draw_text('*', 40, YELLOW, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.app.window.blit(self.app.display, (0, 0))
        pygame.display.update()
        self.app.reset_keys()


class MainMenu(Menu):
    def __init__(self, app):
        Menu.__init__(self, app)
        self.state = 'Start'

        # POS COORDINATES FOR THE MENU BUTTONS
        self.start_button_x, self.start_button_y = self.mid_w, self.mid_h + 50
        self.algorithm_button_x, self.algorithm_button_y = self.mid_w, self.mid_h + 90
        self.tutorial_button_x, self.tutorial_button_y = self.mid_w, self.mid_h + 130

        # CURSOR INITIAL POSITION
        self.cursor_rect.midtop = (self.start_button_x + self.offset, self.start_button_y)

        # COLOR FOR THE MENU BUTTONS
        self.start_button_color, self.algorithm_button_color, self.tutorial_button_color = YELLOW, WHITE, WHITE

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.app.check_events()
            self.check_selection()
            self.app.display.fill(BLACK)
            self.app.display.blit(self.background, (0, 0))
            self.draw_cursor()
            #self.app.draw_text('PATHFINDING-VISUALIZER', 60, WHITE, self.mid_w, 175)
            self.app.draw_text('MAIN MENU', 55, WHITE, self.mid_w, self.mid_h - 20)
            self.app.draw_text('START VISUALIZER', 40, self.start_button_color, self.start_button_x, self.start_button_y)
            self.app.draw_text('ALGORITHM', 40, self.algorithm_button_color, self.algorithm_button_x, self.algorithm_button_y)
            self.app.draw_text('TUTORIAL', 40, self.tutorial_button_color,  self.tutorial_button_x, self.tutorial_button_y)
            self.app.draw_text('BY SENAY.G', 22, WHITE, self.app.display_w - 95, self.app.display_h - 15)


            self.blit_screen()

    def move_cursor(self):
        if self.app.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.algorithm_button_x + self.offset, self.algorithm_button_y)
                self.start_button_color = WHITE
                self.algorithm_button_color = YELLOW  # HIGHLIGHTED BUTTON
                self.state = 'Algorithm'

            elif self.state == 'Algorithm':
                self.cursor_rect.midtop = (self.tutorial_button_x + self.offset, self.tutorial_button_y)
                self.algorithm_button_color = WHITE
                self.tutorial_button_color = YELLOW
                self.state = 'Tutorial'

        if self.app.UP_KEY:
            if self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.algorithm_button_x + self.offset, self.algorithm_button_y)
                self.algorithm_button_color = YELLOW
                self.tutorial_button_color = WHITE
                self.state = 'Algorithm'

            elif self.state == 'Algorithm':
                self.cursor_rect.midtop = (self.start_button_x + self.offset, self.start_button_y)
                self.algorithm_button_color = WHITE
                self.start_button_color = YELLOW
                self.state = 'Start'

    def check_selection(self):
        self.move_cursor()
        if self.app.ENTER_KEY:
            if self.state == 'Start':
                self.app.playing = True
            elif self.state == 'Algorithm':
                self.app.menu_screen = self.app.algorithm_menu
            elif self.state == 'Tutorial':
                self.app.menu_screen = self.app.tutorial_menu
            self.run_display = False


class AlgorithmMenu(Menu):
    def __init__(self, app):
        Menu.__init__(self, app)
        self.state = app.search_algorithm

        # POS COORDINATES FOR THE ALGORITHM MENU BUTTONS
        self.astar_button_x, self.astar_button_y = self.mid_w, self.mid_h + 60
        self.dijkstra_button_x, self.dijkstra_button_y = self.mid_w, self.mid_h + 90

        # CURSOR INITIAL POSITION
        if app.search_algorithm == 'A*':
            self.cursor_rect.midtop = self.astar_button_x + self.offset, self.astar_button_y
        elif app.search_algorithm == 'Dijkstra':
            self.cursor_rect.midtop = self.dijkstra_button_x + self.offset, self.dijkstra_button_y


        # MENU BUTTON COLORS
        self.astar_button_color, self.dijkstra_button_color = YELLOW, WHITE

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.app.check_events()
            self.check_selection()
            self.app.display.fill(BLACK)
            self.app.display.blit(self.background, (0, 0))
            self.draw_cursor()
            self.app.draw_text('ALGORITHM', 45, WHITE, self.mid_w, self.mid_h + 10)
            self.app.draw_text('A STAR ALGORITHM', 30, self.astar_button_color, self.astar_button_x,
                               self.astar_button_y)
            self.app.draw_text("DIJKSTRA'S ALGORITHM", 30, self.dijkstra_button_color, self.dijkstra_button_x,
                               self.dijkstra_button_y)
            self.app.draw_text('BY SENAY.G', 22, WHITE, self.app.display_w - 95, self.app.display_h - 15)
            self.blit_screen()

    def move_cursor(self):
        if self.app.DOWN_KEY and self.state == 'A*':
            self.cursor_rect.midtop = (self.dijkstra_button_x + self.offset, self.dijkstra_button_y)
            self.astar_button_color = WHITE
            self.dijkstra_button_color = YELLOW  # HIGHLIGHTED BUTTON
            self.state = 'Dijkstra'

        if self.app.UP_KEY and self.state == 'Dijkstra':
            self.cursor_rect.midtop = (self.astar_button_x + self.offset, self.astar_button_y)
            self.astar_button_color = YELLOW
            self.dijkstra_button_color = WHITE
            self.state = 'A*'

    def check_selection(self):
        self.move_cursor()
        if self.app.ESC_KEY or self.app.BACK_KEY:
            self.app.menu_screen = self.app.main_menu
            self.run_display = False
        if self.app.ENTER_KEY:
            if self.state == 'A*':
                self.app.search_algorithm = 'A*'
            elif self.state == 'Dijkstra':
                self.app.search_algorithm = 'Dijkstra'

            self.app.menu_screen = self.app.main_menu
            self.run_display = False

class TutorialMenu(Menu):
    def __init__(self, app):
        Menu.__init__(self, app)

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.app.check_events()
            self.check_selection()
            self.app.display.fill(BLACK)
            self.app.display.blit(self.background, (0, 0))
            self.app.draw_text('TUTORIAL', 45, WHITE, self.mid_w, self.mid_h + 10)
            self.app.draw_text('FROM THE MAIN MENU SELECT A PATHFINDING ALGORITHM.', 22, WHITE, self.mid_w, self.mid_h + 60)
            self.app.draw_text('WHEN YOU START THE VISUALIZER USE THE LEFT MOUSE CLICK TO',
                               22, WHITE, self.mid_w, self.mid_h + 90)
            self.app.draw_text('PLACE THE START NODE END NODE AND OBSTACLE NODES ON THE GRID.', 22, WHITE, self.mid_w,
                               self.mid_h + 120)
            self.app.draw_text("PRESS 'M' ON YOUR KEYBOARD TO GENERATE A RECURSIVE MAZE.", 22, WHITE, self.mid_w, self.mid_h + 150)
            self.app.draw_text('PRESS THE SPACE KEY TO VISUALIZE THE PATH FINDING ALGORITHM.', 22, WHITE, self.mid_w,
                               self.mid_h + 180)
            self.app.draw_text('USE THE RIGHT MOUSE CLICK TO RESET ANY NODE DRAWN ON THE GRID.', 22, WHITE, self.mid_w, self.mid_h + 210)
            self.app.draw_text("PRESS 'C' ON YOUR KEYBOARD TO CLEAR THE WHOLE GRID.", 22, WHITE, self.mid_w, self.mid_h + 240)
            self.app.draw_text("PRESS 'ESC' OR 'BACKSPACE' KEY TO RETURN TO THE MAIN MENU.", 22, WHITE, self.mid_w, self.mid_h + 270)
            self.app.draw_text('BY SENAY.G', 22, WHITE, self.app.display_w - 95, self.app.display_h - 15)
            self.blit_screen()

    def check_selection(self):
        if self.app.ESC_KEY or self.app.BACK_KEY or self.app.ENTER_KEY:
            self.app.menu_screen = self.app.main_menu
            self.run_display = False
