import pygame
from app import App


def main():
    visualizer = App()
    while visualizer.running:
        visualizer.menu_screen.display_menu()
        visualizer.app_loop()

    pygame.quit()


if __name__ == '__main__':
    main()
