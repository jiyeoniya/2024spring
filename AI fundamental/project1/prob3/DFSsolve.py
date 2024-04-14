import matplotlib.pyplot as plt
import numpy as np

def visualize_maze_with_searched(maze, searched, path, title="Maze Search"):
    plt.figure(figsize=(len(maze[0]), len(maze)))
    color_map = np.array(maze, dtype=float)
    for (x, y) in searched:
        color_map[x][y] = 0.5  # Mark searched nodes
    for (x, y) in path:
        color_map[x][y] = 0.2  # Mark path nodes

    plt.title(title)
    plt.imshow(color_map, cmap='Greys', interpolation='nearest')
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, marker='o', markersize=5, color='red', linewidth=2)
    plt.xticks(range(len(maze[0])))
    plt.yticks(range(len(maze)))
    plt.grid(which="minor", color="black", linestyle='-', linewidth=2)
    plt.gca().set_xticks([x - 0.5 for x in range(1, len(maze[0]))], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, len(maze))], minor=True)
    plt.show()


from queue import Queue

# Example Maze
n, m = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(n)]
start = (0, 0)
goal = (n - 1, m - 1)


def dfs_search(maze, start, goal):
    stack = [(start, [start])]  # (current_position, path_to_current)
    visited = set([start])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        current, path = stack.pop()
        if current == goal:
            return visited, path

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[0]][
                neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return visited, []


visited, path = dfs_search(maze, start, goal)
print(len(path) - 1)
visualize_maze_with_searched(maze, visited, path, title="DFS Search")
