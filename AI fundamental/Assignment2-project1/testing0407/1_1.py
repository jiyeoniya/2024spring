from collections import deque
import time



def shortest_path(n, m, edges):
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)

    dist = [-1] * (n + 1)
    dist[1] = 0

    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

    return dist[n]


# 读取输入
n, m = map(int, input().split())
# start = time.perf_counter()
edges = [list(map(int, input().split())) for _ in range(m)]

# 调用函数并输出结果
result = shortest_path(n, m, edges)
print(result)
# end = time.perf_counter()
# runTime = end - start
# print("运行时间：", runTime)
