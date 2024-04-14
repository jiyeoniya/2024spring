from collections import deque
import matplotlib.pyplot as plt
import numpy as np


def bfs(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = np.zeros_like(maze)  # 使用与迷宫相同维度的数组记录访问状态
    visited[start[0]][start[1]] = 1
    parent = {}  # 记录每个位置的父节点，用于回溯路径

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return visited, parent

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and visited[nx][ny] == 0:
                visited[nx][ny] = 1
                parent[(nx, ny)] = (x, y)  # 记录父节点
                queue.append((nx, ny))

    return visited, parent


def reconstruct_path(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def visualize_maze_with_paths(maze, visited, shortest_path):
    plt.figure(figsize=(len(maze[0]), len(maze)))
    plt.imshow(maze, cmap='Greys', interpolation='nearest')

    if np.any(visited):  # 如果有访问过的位置
        visited_x, visited_y = np.where(visited == 1)
        plt.plot(visited_y, visited_x, marker='o', markersize=8, color='lightgrey', linestyle='',
                 label='Visited Cells')

    if shortest_path:
        shortest_path_x, shortest_path_y = zip(*shortest_path)
        plt.plot(shortest_path_y, shortest_path_x, marker='', markersize=8, color='red', linewidth=3,
                 linestyle='-', label='Shortest Path')

    plt.legend(loc='upper right')
    plt.xticks(range(len(maze[0])))
    plt.yticks(range(len(maze)))
    plt.gca().set_xticks([x - 0.5 for x in range(1, len(maze[0]))], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, len(maze))], minor=True)
    plt.grid(which="minor", color="black", linestyle='-', linewidth=2)

    plt.axis('on')
    plt.show()


# 读取输入的迷宫大小和内容
n, m = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(n)]

start = (0, 0)
end = (n - 1, m - 1)

# 使用BFS算法搜索并记录所有被访问过的格子以及路径
visited, parent = bfs(maze, start, end)
shortest_path = reconstruct_path(parent, start, end)

# 可视化迷宫及路径
visualize_maze_with_paths(maze, visited, shortest_path)
