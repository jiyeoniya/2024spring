from queue import PriorityQueue
import time

# 计算逆序数
def count_inversions(arr):
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] != 'x' and arr[j] != 'x' and arr[i] > arr[j]:
                inversions += 1
    return inversions


# 启发函数，计算当前状态到目标状态的曼哈顿距离
def heuristic(state):
    manhattan_distance = 0
    for i in range(9):
        if state[i] != 'x':
            current_row, current_col = i // 3, i % 3
            target_row, target_col = (int(state[i]) - 1) // 3, (int(state[i]) - 1) % 3
            manhattan_distance += abs(current_row - target_row) + abs(current_col - target_col)
    return manhattan_distance


# 移动操作
def move(state, direction):
    new_state = list(state)
    x_index = state.index('x')
    if direction == 'u':
        new_state[x_index], new_state[x_index - 3] = new_state[x_index - 3], new_state[x_index]
    elif direction == 'd':
        new_state[x_index], new_state[x_index + 3] = new_state[x_index + 3], new_state[x_index]
    elif direction == 'l':
        new_state[x_index], new_state[x_index - 1] = new_state[x_index - 1], new_state[x_index]
    elif direction == 'r':
        new_state[x_index], new_state[x_index + 1] = new_state[x_index + 1], new_state[x_index]
    return ''.join(new_state)


# A*算法
def astar(start):
    directions = ['u', 'd', 'l', 'r']
    pq = PriorityQueue()
    pq.put((heuristic(start), start, '', 0))
    visited = set()

    while not pq.empty():
        _, state, path, cost = pq.get()
        if state == '12345678x':
            return path

        visited.add(state)
        x_index = state.index('x')
        for direction in directions:
            if (direction == 'u' and x_index < 3) or (direction == 'd' and x_index > 5) or (
                    direction == 'l' and x_index % 3 == 0) or (direction == 'r' and x_index % 3 == 2):
                continue
            new_state = move(state, direction)
            if new_state not in visited:
                new_cost = cost + 1
                pq.put((new_cost + heuristic(new_state), new_state, path + direction, new_cost))

    return "unsolvable"


# 输入处理
a = input().strip()
# start = time.perf_counter()
input_str = a
start_state = input_str.replace(' ', '')

# 解决八数码问题
result = astar(start_state)
print(result)
# end = time.perf_counter()
# runTime = end - start
# print("运行时间：", runTime)