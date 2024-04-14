from queue import Queue
import time

# start = time.perf_counter()
def count_inversions(arr):
    inversions = 0
    for i in range(len(arr)):
        if arr[i] == 'x':
            continue
        for j in range(i + 1, len(arr)):
            if arr[j] != 'x' and arr[i] > arr[j]:
                inversions += 1
    return inversions


# 定义方向数组，分别表示上、下、左、右四个方向
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3


def solve_puzzle(grid):
    start_state = grid.split()
    target_state = ['1', '2', '3', '4', '5', '6', '7', '8', 'x']

    # 计算逆序数
    inversions_start = count_inversions(start_state)
    inversions_target = count_inversions(target_state)

    # 判断问题是否有解
    if inversions_start % 2 != inversions_target % 2:
        return -1

    start_state = tuple(start_state)

    q = Queue()
    q.put((start_state, 0))
    visited = {start_state}

    while not q.empty():
        state, depth = q.get()

        if state == tuple(target_state):
            return depth

        zero_index = state.index('x')
        zero_x, zero_y = zero_index // 3, zero_index % 3

        for dx, dy in directions:
            new_x, new_y = zero_x + dx, zero_y + dy
            if is_valid_move(new_x, new_y):
                new_zero_index = new_x * 3 + new_y
                new_state = list(state)
                new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[zero_index]
                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    q.put((new_state, depth + 1))

    return -1  # 如果没有找到解，返回-1


# 读取输入
initial_grid = input().strip()
# start = time.perf_counter()
# 求解问题并输出结果
print(solve_puzzle(initial_grid))

# end = time.perf_counter()
# runTime = end - start
# print("运行时间：", runTime)