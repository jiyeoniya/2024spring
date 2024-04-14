def is_solvable(board):
    # 计算空白格从初始状态到目标状态的奇偶性
    blank_to_target = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if board[i] != 'x' and board[j] != 'x' and int(board[i]) > int(board[j]):
                blank_to_target += 1

    # 如果空白格移动奇偶性与初始状态到目标状态的奇偶性相同，则问题有解
    return blank_to_target % 2 == 0


def dfs(board, depth, x_pos, visited, max_depth):
    if depth > max_depth:
        return float('inf')

    if board == '12345678x':
        return depth

    # 上、下、左、右四个方向的偏移量
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    min_moves = float('inf')

    for i in range(4):
        nx, ny = x_pos // 3 + dx[i], x_pos % 3 + dy[i]
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_x_pos = nx * 3 + ny
            new_board = list(board)
            new_board[x_pos], new_board[new_x_pos] = new_board[new_x_pos], new_board[x_pos]
            new_board = ''.join(new_board)

            if new_board not in visited:
                visited.add(new_board)
                moves = dfs(new_board, depth + 1, new_x_pos, visited, max_depth)
                min_moves = min(min_moves, moves)

    return min_moves


def main():
    initial_board = input().split()
    initial_board = ''.join(initial_board)

    if is_solvable(initial_board):
        x_pos = initial_board.index('x')
        visited = set()
        visited.add(initial_board)
        max_depth = 50  # 设置最大递归深度
        moves = dfs(initial_board, 0, x_pos, visited, max_depth)
        print(1)
    else:
        print(0)


if __name__ == "__main__":
    main()