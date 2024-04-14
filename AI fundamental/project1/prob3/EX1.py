import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import random

# 画布
fig, ax = plt.subplots()


class Map:  # 地图
    def __init__(self, width, height) -> None:
        # 迷宫的尺寸
        self.width = width
        self.height = height
        # 创建size x size 的点的邻接表
        self.neighbor = [[] for i in range(width * height)]

    def addEdge(self, from_: int, to_: int):  # 添加边
        if (from_ not in range(self.width * self.height)) or (to_ not in range(self.width * self.height)):
            return 0
        self.neighbor[from_].append(to_)
        self.neighbor[to_].append(from_)
        return 1

    def get_x_y(self, num: int):  # 由序号获得该点在迷宫的x、y坐标
        if num not in range(self.width * self.height):
            return -1, -1
        x = num % self.width
        y = num // self.width
        return x, y

    def drawCircle(self, num, color):  # 绘制圆形
        x, y = self.get_x_y(num)
        thePoint = mpathes.Circle(np.array([x + 1, y + 1]), 0.1, color=color)
        # 声明全局变量
        global ax
        ax.add_patch(thePoint)

    def drawEdge(self, from_, to_, color):  # 绘制边
        # 转化为(x,y)
        x1, y1 = self.get_x_y(from_)
        x2, y2 = self.get_x_y(to_)
        # 整体向右下方移动一个单位
        x1, y1 = x1 + 1, y1 + 1
        x2, y2 = x2 + 1, y2 + 1
        # 绘长方形代表边
        offset = 0.05
        global ax
        if from_ - to_ == 1:  # ← 方向的边
            rect = mpathes.Rectangle(
                np.array([x2 - offset, y2 - offset]), 1 + 2 * offset, 2 * offset, color=color)
            ax.add_patch(rect)
        elif from_ - to_ == -1:  # → 方向的边
            rect = mpathes.Rectangle(
                np.array([x1 - offset, y1 - offset]), 1 + 2 * offset, 2 * offset, color=color)
            ax.add_patch(rect)
        elif from_ - to_ == self.width:  # ↑ 方向的边
            rect = mpathes.Rectangle(
                np.array([x2 - offset, y2 - offset]), 2 * offset, 1 + 2 * offset, color=color)
            ax.add_patch(rect)
        else:  # ↓ 方向的边
            rect = mpathes.Rectangle(
                np.array([x1 - offset, y1 - offset]), 2 * offset, 1 + 2 * offset, color=color)
            ax.add_patch(rect)

    def initMap(self):  # 绘制初始的迷宫
        # 先绘制边
        for i in range(self.width * self.height):
            for next in self.neighbor[i]:
                self.drawEdge(i, next, '#afeeee')

        # 再绘制点
        for i in range(self.width * self.height):
            self.drawCircle(i, '#87cefa')

    # 寻找
    def search(self, current: int):
        # 四个方向的顺序
        sequence = [i for i in range(4)]
        # 打乱顺序
        random.shuffle(sequence)
        # 依次选择四个方向
        for i in sequence:
            # 要探索的位置
            x = self.direction[i] + current

            # 跨了一行
            if (current % self.width == self.width - 1 and self.direction[i] == 1) or (
                    current % self.width == 0 and self.direction[i] == -1):
                continue

            # 要探索的位置没有超出范围 且 该位置没有被探索过
            if 0 <= x < self.width * self.height and self.visited[x] == 0:
                self.addEdge(current, x)
                self.visited[x] = 1
                self.search(x)

    # 随机添加k条边
    def randomAddEdges(self, k):
        # 循环k次(可能不止k次)
        for i in range(k):
            node = random.randint(0, self.width * self.height)
            # 随机添加一个方向
            sequence = [i for i in range(4)]
            random.shuffle(sequence)
            isPick = 0
            for d in sequence:
                # 跨了一行,不存在该方向的边
                if (node % self.width == self.width - 1 and self.direction[d] == 1) or (
                        node % self.width == 0 and self.direction[d] == -1):
                    continue
                x = self.direction[d] + node
                # 该边存在
                if x in self.neighbor[node]:
                    continue
                # 该边不存在
                self.addEdge(node, x)
                isPick = 1
            # 重新添加一条边,即重新循环一次
            if isPick == 0:
                if i == 0:  # 第一次
                    i = 0
                else:
                    i -= 1

    def randomCreateMap(self, start, k):  # 随机生成迷宫
        # 标识每个节点是否被探索过
        self.visited = np.zeros(self.width * self.height)
        self.visited[start] = 1
        # 四个方向,分别代表上、下、左、右
        self.direction = {0: -self.width,
                          1: self.width,
                          2: -1,
                          3: 1}
        # 从起点开始
        self.search(start)
        # 随机添加k条边，使得迷宫尽可能出现多条到达终点的路径
        self.randomAddEdges(k)


class Astar:  # A*寻路算法
    def __init__(self, _map: Map, start: int, end: int) -> None:
        # 地图
        self.run_map = _map
        # 起点和终点
        self.start = start
        self.end = end
        # open集
        self.open_set = PriorityQueue()
        # cost_so_far表示到达某个节点的代价，也可相当于close集使用
        self.cost_so_far = dict()
        # 每个节点的前序节点
        self.came_from = dict()

        # 将起点放入,优先级设为0，无所谓设置多少，因为总是第一个被取出
        self.open_set.put((0, start))
        self.came_from[start] = -1
        self.cost_so_far[start] = 0

        # 标识起点和终点
        self.run_map.drawCircle(start, '#ff8099')
        self.run_map.drawCircle(end, '#ff4d40')

    def heuristic(self, a, b):  # h函数计算,即启发式信息
        x1, y1 = self.run_map.get_x_y(a)
        x2, y2 = self.run_map.get_x_y(b)
        return abs(x1 - x2) + abs(y1 - y2)

    def find_way(self):  # 运行A*寻路算法，如果没找到路径返回0，找到返回1
        while not self.open_set.empty():  # open表不为空
            # 从优先队列中取出代价最短的节点作为当前遍历的节点，类型为(priority,node)
            current = self.open_set.get()

            # 展示A*算法的执行过程
            if current[1] != self.start:
                # 当前节点的前序
                pre = self.came_from[current[1]]
                # 可视化
                self.run_map.drawEdge(pre, current[1], '#fffdd0')
                if pre != self.start:
                    self.run_map.drawCircle(pre, '#99ff4d')
                else:  # 起点不改色
                    self.run_map.drawCircle(pre, '#ff8099')
                if current[1] != self.end:
                    self.run_map.drawCircle(current[1], '#99ff4d')
                else:
                    self.run_map.drawCircle(current[1], '#ff4d40')
                # 显示当前状态
                plt.show()
                plt.pause(0.01)

            # 找到终点
            if current[1] == self.end:
                break
            # 遍历邻接节点
            for next in self.run_map.neighbor[current[1]]:
                # 新的代价
                new_cost = self.cost_so_far[current[1]] + 1
                # 没有到达过的点 或 比原本已经到达过的点的代价更小
                if (next not in self.cost_so_far) or (new_cost < self.cost_so_far[next]):
                    self.cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, self.end)
                    self.open_set.put((priority, next))
                    self.came_from[next] = current[1]

    def show_way(self):  # 显示最短路径
        # 记录路径经过的节点
        result = []
        current = self.end

        if current not in self.cost_so_far:
            return

        # 不断寻找前序节点
        while self.came_from[current] != -1:
            result.append(current)
            current = self.came_from[current]
        # 加上起点
        result.append(current)
        # 翻转路径
        result.reverse()
        # 生成路径
        for point in result:
            if point != self.start:  # 不是起点
                # 当前节点的前序
                pre = self.came_from[point]
                # 可视化
                self.run_map.drawEdge(pre, point, '#ff2f76')
                if pre == self.start:  # 起点颜色
                    self.run_map.drawCircle(pre, '#ff8099')
                elif point == self.end:  # 终点颜色
                    self.run_map.drawCircle(point, '#ff4d40')
                # 显示当前状态
                plt.show()
                plt.pause(0.005)

    def get_cost(self):  # 返回最短路径
        if self.end not in self.cost_so_far:
            return -1
        return self.cost_so_far[self.end]


# 初始化迷宫，设置宽度和高度
theMap = Map(20, 20)

# 设置迷宫显示的一些参数
plt.xlim(0, theMap.width + 1)
plt.ylim(0, theMap.height + 1)
# 将x轴的位置设置在顶部
ax.xaxis.set_ticks_position('top')
# y轴反向
ax.invert_yaxis()
# 等距
plt.axis('equal')
# 不显示背景的网格线
plt.grid(False)
# 允许动态
plt.ion()

# 随机添加边，生成迷宫，第一个参数为起点；第二个参数为额外随机生成的边，可以表示为图的复杂程度
theMap.randomCreateMap(0, 20)

# 初始化迷宫
theMap.initMap()

# A* 算法寻路
theAstar = Astar(theMap, 0, 399)  # 设置起点和终点
theAstar.find_way()  # 寻路
theAstar.show_way()  # 显示最短路径

# 输出最短路径长度
theCost = theAstar.get_cost()
if theCost == -1:
    print("不存在该路径！")
else:
    print("从起点到终点的最短路径长度为: ", theCost)

# 关闭交互，展示结果
plt.ioff()
plt.show()