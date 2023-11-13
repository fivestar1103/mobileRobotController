import heapq
from typing import List
from Path_Planning_and_Map_Management.Map import Map


class PathPlanner:
    def __init__(self, mapObject: Map):
        self.__map = mapObject
        self.__currentPath = []

    # 현재 경로를 반환
    def get_current_path(self):
        return self.__currentPath

    # 현재 경로를 설정
    def set_current_path(self, path: List[List]):
        self.__currentPath = path

    # -------- a* 알고리즘 구현에 필요한 함수들 ------- #
    def __heuristic(self, a, b):  # 맨해튼 거리 이용
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def __get_neighbors(self, node):  # 상하좌우 이웃을 반환
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            cols, rows = self.__map.get_map_length()
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows:
                neighbors.append(neighbor)
        return neighbors

    def __a_star_search(self, start, goal, hazards):
        frontier = []
        heapq.heappush(frontier, (0, start))
        cameFrom = {start: None}
        costSoFar = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in self.__get_neighbors(current):
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
        # path.append(start)  # 시작점 추가
        path.reverse()  # 시작점부터 경로를 재구성
        return path

    # ----------------------------------- #

    # 최단 경로 구하기
    def plan_path(self):
        self.__map.print_full_map()

        start = self.__map.get_robot_coord()  # 로봇의 현재 위치
        goals = [spot.get_position() for spot in self.__map.get_spots() if not spot.is_explored()]  # 방문하지 않은 탐색 지점
        hazards = {hazard.get_position() for hazard in self.__map.get_hazards() if not hazard.is_hidden()}  # 공개된 위험 지점
        path = [start]

        while goals:
            next_goal = min(goals, key=lambda x: self.__heuristic(path[-1], x))
            goals.remove(next_goal)
            subpath = self.__a_star_search(path[-1], next_goal, hazards)
            if subpath:  # 경로가 존재하는 경우에만 추가
                path.extend(subpath)  # 시작점을 제외하고 경로 추가
            else:
                # 경로가 존재하지 않는 경우
                print("No path exists!")
                return

        pathStack = path[1:]
        pathStack.reverse()
        self.set_current_path(pathStack)
