import heapq
import time


def dijkstra(n, edges):
    graph = {i: [] for i in range(1, n + 1)}
    for x, y, z in edges:
        graph[x].append((y, z))

    dist = [float('inf')] * (n + 1)
    dist[1] = 0

    pq = []
    heapq.heappush(pq, (0, 1))

    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            if d + weight < dist[neighbor]:
                dist[neighbor] = d + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))

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