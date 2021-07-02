import pygame
from queue import PriorityQueue


def h_cost(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


class Algorithm:
    def __init__(self, board):
        self.board = board
        # self.start = start
        # self.end = end

    def astar(self, start, end):
        count = 0  # count keeps track of when we added a node to the queue and will be used to break ties
        open_nodes = PriorityQueue()
        f_score = 0
        open_nodes.put((f_score, count, start))
        came_from = {}
        g_cost = {node: float("inf") for row in self.board.grid for node in row}
        g_cost[start] = 0
        f_cost = {node: float("inf") for row in self.board.grid for node in row}
        f_cost[start] = h_cost(start.get_pos(), end.get_pos()) + g_cost[start]

        open_nodes_hash = {start}

        while not open_nodes.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_nodes.get()[2]  # dequeue the highest priority node (node with the smallest f_cost)
            open_nodes_hash.remove(current)

            if current == end:
                end.make_end()
                self.board.show_path(current, start, came_from)
                # draw
                return True

            for neighbor in current.neighbors:
                temp_g_cost = g_cost[current] + 1

                if temp_g_cost < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = temp_g_cost
                    f_cost[neighbor] = h_cost(neighbor.get_pos(), end.get_pos()) + g_cost[neighbor]
                    if neighbor not in open_nodes_hash:
                        count += 1
                        open_nodes.put((f_cost[neighbor], count, neighbor))
                        open_nodes_hash.add(neighbor)
                        neighbor.make_open()

            self.board.draw()

            if current != start:
                current.make_closed()

    def dijkstra(self, start, end):
        count = 0  # count keeps track of when we added a node to the queue and will be used to break ties
        open_nodes = PriorityQueue()
        cost = 0
        open_nodes.put((cost, count, start))
        came_from = {}
        total_cost = {node: float("inf") for row in self.board.grid for node in row}
        total_cost[start] = 0
        open_nodes_hash = {start}

        while not open_nodes.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_nodes.get()[2]  # dequeue the highest priority node (node with the smallest f_cost)
            open_nodes_hash.remove(current)

            if current == end:
                end.make_end()
                self.board.show_path(current, start, came_from)
                # draw
                return True

            for neighbor in current.neighbors:
                temp_cost = total_cost[current] + 1

                if temp_cost < total_cost[neighbor]:
                    came_from[neighbor] = current
                    total_cost[neighbor] = temp_cost
                    if neighbor not in open_nodes_hash:
                        count += 1
                        open_nodes.put((total_cost[neighbor], count, neighbor))
                        open_nodes_hash.add(neighbor)
                        neighbor.make_open()

            self.board.draw()

            if current != start:
                current.make_closed()