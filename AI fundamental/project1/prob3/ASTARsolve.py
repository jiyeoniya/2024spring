import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue


def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(maze, start, goal):
    """Performs A* search from start to goal in the given maze."""
    neighbor_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右, 下, 左, 上
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    searched = set()

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            break

        for direction in neighbor_directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                if maze[neighbor[0]][neighbor[1]] != 1:  # Check if the neighbor is walkable
                    new_cost = cost_so_far[current] + 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + heuristic(goal, neighbor)
                        open_set.put((priority, neighbor))
                        came_from[neighbor] = current
                        searched.add(neighbor)

    return came_from, searched


def reconstruct_path(came_from, start, goal):
    """Reconstructs the path from start to goal using the came_from dictionary."""
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def visualize_maze_with_path(maze, path, searched):
    plt.figure(figsize=(len(maze[0]), len(maze)))
    plt.imshow(maze, cmap='Greys', interpolation='nearest')
    for s in searched:
        if s not in path:
            plt.plot(s[1], s[0], marker='o', markersize=5, color='pink')
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, marker='o', markersize=8, color='red', linewidth=3)
    plt.xticks(range(len(maze[0])))
    plt.yticks(range(len(maze)))
    plt.gca().set_xticks([x - 0.5 for x in range(1, len(maze[0]))], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, len(maze))], minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=2)
    plt.axis('on')
    plt.show()


# Define the maze and start/goal positions

n, m = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(n)]
start = (0, 0)
goal = (n - 1, m - 1)

came_from, searched = a_star_search(maze, start, goal)
path = reconstruct_path(came_from, start, goal)
print(len(path) - 1)
visualize_maze_with_path(maze, path, searched)
