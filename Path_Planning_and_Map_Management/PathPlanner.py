import heapq
from typing import List
from Path_Planning_and_Map_Management.Map import Map
class PathPlanner:
    def __init__(self, mapObject: Map):
        self.__map = mapObject
        self.__currentPath = []

    # 현재 경로를 반환
    def getCurrentPath(self):
        return self.__currentPath

    # 현재 경로를 설정
    def setCurrentPath(self, path: List[List]):
        self.__currentPath = path

    # -------- a* 알고리즘 구현에 필요한 함수들 ------- #
    def __heuristic(self, a, b):  # 맨해튼 거리 이용
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def __getNeighbors(self, node):  # 상하좌우 이웃을 반환
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            cols, rows = self.__map.getMapLength()
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows:
                neighbors.append(neighbor)
        return neighbors

    def __aStarSearch(self, start, goal, hazards):
        frontier = []
        heapq.heappush(frontier, (0, start))
        cameFrom = {start: None}
        costSoFar = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in self.__getNeighbors(current):
                if next in hazards:
                    continue  # 위험 지점은 무시
                newCost = costSoFar[current] + 1  # 모든 이동 비용은 1로 가정
                if next not in costSoFar or newCost < costSoFar[next]:
                    costSoFar[next] = newCost
                    priority = newCost + self.__heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    cameFrom[next] = current

        # 경로 재구성
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = cameFrom[current]
        path.append(start)  # 시작점 추가
        path.reverse()  # 시작점부터 경로를 재구성
        return path

    # ----------------------------------- #

    # 최단 경로 구하기
    def planPath(self):
        fullMap = self.__map.getFullMap()
        numberIconString = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        # print the fullMap
        print("########## 🗺️ Map: ##########")
        cols, rows = self.__map.getMapLength()
        for row in reversed(fullMap):
            print(f"{numberIconString[rows - 1]}", end=' ')
            rows -= 1
            for col in row:
                print(col, end=' ')
            print()
        print("  ", end=' ')
        for colNum in range(cols):
            print(f"{numberIconString[colNum]}", end=' ')
        print()


        start = self.__map.getRobotCoord()  # 로봇의 현재 위치
        goals = [spot.getPosition() for spot in self.__map.getSpots() if not spot.isExplored()]  # 방문하지 않은 탐색 지점
        hazards = {hazard.getPosition() for hazard in self.__map.getHazards() if not hazard.isHidden()}  # 공개된 위험 지점
        path = [start]

        while goals:
            next_goal = min(goals, key=lambda x: self.__heuristic(path[-1], x))
            goals.remove(next_goal)
            subpath = self.__aStarSearch(path[-1], next_goal, hazards)
            if subpath:  # 경로가 존재하는 경우에만 추가
                path.extend(subpath[1:])  # 시작점을 제외하고 경로 추가
            else:
                # 경로가 존재하지 않는 경우
                print("No path exists!")
                return

        self.__currentPath = path
        return self.__currentPath

