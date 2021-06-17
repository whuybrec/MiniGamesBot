import copy
import math
import random
from queue import PriorityQueue

from generic.formatting import create_table
from minigames.minigame import Minigame

COLORS = ["blue", "red", "purple", "yellow", "green", "orange"]

WIDTH = HEIGHT = 10
MOVES_FACTOR = 8


class Grid:
    def __init__(self, grid=None, moves=0):
        if grid is None:
            self.set_random_grid()
        else:
            self.matrix = copy.deepcopy(grid)
        self.colors = set()
        self.moves = moves
        self.cost = 0
        self.heuristic()
        self.set_colors()

    def pick_color(self, picked_color):
        top_node = self.matrix[0][0]
        old_color = top_node.color
        top_node.color = picked_color
        queue = [top_node]
        visited = set()

        while len(queue) > 0:
            node = queue.pop()
            visited.add(node)
            neighbours = self.expand_node(node)
            for neighbour in neighbours:
                if neighbour.color == old_color:
                    neighbour.color = picked_color
                    if neighbour not in visited:
                        queue.append(neighbour)
        self.heuristic()
        self.set_colors()

    def expand_node(self, node):
        x = node.x
        y = node.y
        up = self.matrix[(x - 1) if (x - 1) >= 0 else 0][y]
        down = self.matrix[(x + 1) if (x + 1) < HEIGHT else (HEIGHT - 1)][y]
        left = self.matrix[x][(y - 1) if (y - 1) >= 0 else 0]
        right = self.matrix[x][(y + 1) if (y + 1) < WIDTH else (WIDTH - 1)]
        return [up, down, left, right]

    def set_random_grid(self):
        self.matrix = []
        for i in range(HEIGHT):
            self.matrix.append([Node(i, j, COLORS[random.randint(0, len(COLORS) - 1)]) for j in range(WIDTH)])

    def is_solved(self):
        top_color = self.matrix[0][0].color
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.matrix[i][j].color != top_color:
                    return False
        return True

    def heuristic(self):
        top_node = self.matrix[0][0]
        queue = [top_node]
        visited = set()
        size = 0

        while len(queue) > 0:
            node = queue.pop()
            visited.add(node)
            neighbours = self.expand_node(node)
            for neighbour in neighbours:
                if neighbour.color == top_node.color and neighbour not in visited:
                    size += 1
                    queue.append(neighbour)
        self.cost = WIDTH * HEIGHT - size

    def set_colors(self):
        colors = set()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                colors.add(self.matrix[i][j].color)
        self.colors = colors

    def __lt__(self, other):
        return self.moves + self.cost < other.moves + other.cost

    def __gt__(self, other):
        return other.moves + other.cost < self.moves + self.cost

    def __eq__(self, other):
        return create_table(*self.matrix) == create_table(*other.matrix) and self.moves == other.moves

    def __hash__(self):
        return hash(create_table(*self.matrix) + str(self.moves))


class Node:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __hash__(self):
        return hash((self.x, self.y, self.color))


class Flood(Minigame):
    def __init__(self):
        self.grid = Grid()
        self.min_moves = self.solve()
        self.min_allowed_moves = self.min_moves + math.floor(self.min_moves / MOVES_FACTOR)
        self.player_moves = 0

    def pick_color(self, color):
        self.player_moves += 1
        self.grid.pick_color(color)

    def has_won(self):
        return self.player_moves <= self.min_allowed_moves and self.grid.is_solved()

    def has_lost(self):
        return self.player_moves >= self.min_allowed_moves

    def has_drawn(self):
        pass  # can't draw in scramble

    def solve(self):
        queue = PriorityQueue()
        queue.put((0, self.grid))
        visited = set()

        while True:
            parent = queue.get()[1]
            if parent.is_solved():
                break

            visited.add(parent)
            for color in parent.colors:
                if color != parent.matrix[0][0].color:
                    grid = Grid(parent.matrix, parent.moves + 1)
                    grid.pick_color(color)
                    if grid not in visited:
                        queue.put((grid.moves + grid.cost, grid))
        return parent.moves
