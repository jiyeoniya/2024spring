from collections import deque
import matplotlib.pyplot as plt


def bfs(maze, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path + [(x, y)], len(path)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(x, y)]))

    return [], -1


def visualize_maze_with_paths(maze, explored_path, shortest_path):
    plt.figure(figsize=(len(maze[0]), len(maze)))
    plt.imshow(maze, cmap='Greys', interpolation='nearest')

    if explored_path:
        explored_path_x, explored_path_y = zip(*explored_path)
        plt.plot(explored_path_y, explored_path_x, marker='o', markersize=8, color='blue', linestyle='dashed',
                 linewidth=2, label='Explored Path')

    if shortest_path:
        shortest_path_x, shortest_path_y = zip(*shortest_path)
        plt.plot(shortest_path_y, shortest_path_x, marker='o', markersize=8, color='red', linewidth=3,
                 label='Shortest Path')

    plt.legend()
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

# 使用BFS算法求解最短路径
shortest_path, min_steps = bfs(maze, start, end)

# 回溯找到搜索过的路径
explored_path = []
for x in range(n):
    for y in range(m):
        if maze[x][y] == 1:
            explored_path.append((x, y))

# 可视化迷宫及路径
visualize_maze_with_paths(maze, explored_path, shortest_path)

print(min_steps)
