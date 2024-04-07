import time




def dijkstra(n, edges):
    graph = {i: [] for i in range(1, n + 1)}
    for x, y, z in edges:
        graph[x].append((y, z))

    dist = [float('inf')] * (n + 1)
    dist[1] = 0

    visited = [False] * (n + 1)

    for _ in range(n):
        min_dist = float('inf')
        min_node = -1
        for i in range(1, n + 1):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_node = i

        if min_node == -1:
            break

        visited[min_node] = True
        for neighbor, weight in graph[min_node]:
            if not visited[neighbor]:
                dist[neighbor] = min(dist[neighbor], dist[min_node] + weight)

    return dist[n] if dist[n] != float('inf') else -1


# 读取输入
n, m = map(int, input().split())
# start = time.perf_counter()
edges = [list(map(int, input().split())) for _ in range(m)]

# 调用dijkstra函数计算最短距离，并输出结果
print(dijkstra(n, edges))
# end = time.perf_counter()
# runTime = end - start
# print("运行时间：", runTime)