# 이 클래스는 지도 객체를 구현한 것으로, 지도와 관련된 모든 정보와 동작을 다룬다.

from typing import List, Tuple
from Backend.Data_Structures.ColorBlob import ColorBlob
from Backend.Data_Structures.Hazard import Hazard
from Backend.Data_Structures.Spot import Spot


class Map:
    def __init__(self):
        self.__mapLength: Tuple[int, int] = (0, 0)  # colLength, rowLength
        self.__robotCoord: Tuple[int, int, int] = (0, 0, 0)  # col, row, direction(북동남서 순으로 0~4)
        self.__spots: List[Spot] = []
        self.__hazards: List[Hazard] = []
        self.__colorBlobs: List[ColorBlob] = []

    # 지도의 행과 열의 길이를 반환
    def get_map_length(self):
        return self.__mapLength

    # 지도의 행과 열의 길이를 설정
    def set_map_length(self, cols, rows):
        self.__mapLength = (cols, rows)

    # 로봇의 위치 반환
    def get_robot_coord(self):
        return self.__robotCoord

    # 로봇의 위치 설정
    def set_robot_coord(self, position: (int, int, int)):
        self.__robotCoord = position

    # 모든 탐색 지점을 반환
    def get_spots(self):
        return self.__spots

    # 탐색 지점들을 설정
    def set_spots(self, spots: List[Spot]):
        self.__spots = spots

    # 모든 위험 지점을 반환
    def get_hazards(self):
        return self.__hazards

    # 위험 지점들을 생성
    def set_hazards(self, hazards: List[Hazard]):
        self.__hazards = hazards

    # 모든 중요 지점을 반환
    def get_color_blobs(self):
        return self.__colorBlobs

    # 중요 지점을 설정
    def set_color_blobs(self, colorBlobs: List[ColorBlob]):
        self.__colorBlobs = colorBlobs

    # 지도 상의 로봇을 한 칸 앞으로 이동
    def move_robot_on_map(self):
        currentPosition = self.get_robot_coord()
        currentCol, currentRow, currentDirection = currentPosition
        movementAccordingToDirection = {
            0: (0, 1),
            1: (1, 0),
            2: (0, -1),
            3: (-1, 0)
        }
        colDiff, rowDiff = movementAccordingToDirection[currentDirection]
        currentCol += colDiff
        currentRow += rowDiff
        updatedCurrentPosition = (currentCol, currentRow, currentDirection)
        self.set_robot_coord(updatedCurrentPosition)

    # 지도 상의 로봇을 시계 방향으로 90도 회전
    def rotate_robot_on_map(self):
        currentPosition = self.get_robot_coord()
        currentCol, currentRow, currentDirection = currentPosition
        currentDirection = (currentDirection + 1) % 4
        updatedCurrentPosition = (currentCol, currentRow, currentDirection)
        self.set_robot_coord(updatedCurrentPosition)

    # 새로운 지점 추가
    def add_new_points(self, newPoints: List):
        newPointCount = 0
        for newPoint in newPoints:
            if type(newPoint) is Hazard:
                if not any(hazard.get_position() == newPoint.get_position() for hazard in self.get_hazards()):
                    self.__hazards.append(newPoint)
                    newPointCount += 1
                    print("new hazard!")
            elif type(newPoint) is ColorBlob:
                if not any(colorBlob.get_position() == newPoint.get_position() for colorBlob in self.get_color_blobs()):
                    self.__colorBlobs.append(newPoint)
                    newPointCount += 1
                    print("new colorBlob!")
            elif type(newPoint) is Spot:
                if not any(spot.get_position() == newPoint.get_position() for spot in self.get_spots()):
                    self.__spots.append(newPoint)
                    newPointCount += 1
                    print("new spot!")
        print(f"\t{newPointCount} new point(s) have been added...")

    # 숨겨진 지점을 공개된 지점으로 변경
    def reveal_hidden(self, point):
        if isinstance(point, ColorBlob):
            for colorBlob in self.__colorBlobs:
                if point.get_position() == colorBlob.get_position():
                    colorBlob.set_revealed()
        elif isinstance(point, Hazard):
            for hazard in self.__hazards:
                if point.get_position() == hazard.get_position():
                    hazard.set_revealed()

    # 현재 맵에 존재하는 모든 물체들의 위치를 반환
    def get_existing_positions(self):
        existing_positions = [self.get_robot_coord()[:2]]
        for hazard in self.get_hazards():
            existing_positions.append(hazard.get_position())
        for colorBlob in self.get_color_blobs():
            existing_positions.append(colorBlob.get_position())
        for spot in self.get_spots():
            existing_positions.append(spot.get_position())
        return existing_positions

    # 전체 맵 반환 - 디버깅 목적. 실제로는 필요 없음
    def print_full_map(self, whichMap=''):
        # 맵의 크기에 맞는 2차원 배열 생성
        cols, rows = self.get_map_length()
        fullMap = [['⚪󠀠󠀠' for _ in range(cols)] for _ in range(rows)]

        # spots, hazards, colorBlobs를 맵에 표시
        for spot in self.__spots:  # '✅'는 방문한 탐색지점을 의미, '🎯'는 방문하지 않은 탐색지점
            col, row = spot.get_position()
            fullMap[row][col] = '✅' if spot.is_explored() else '🎯'

        for hazard in self.__hazards:  # 'h'는 숨겨진 위험 지점을 의미, '⚠'는 공개된 위험 지점
            col, row = hazard.get_position()
            fullMap[row][col] = 'hh' if hazard.is_hidden() else '⚠️'

        for colorBlob in self.__colorBlobs:  # 'c'는 숨겨진 중요 지점을 의미, '🔵'는 공개된 중요 지점
            col, row = colorBlob.get_position()
            fullMap[row][col] = 'cc' if colorBlob.is_hidden() else '🔵'

        # 로봇의 위치를 맵에 표시
        col, row, direction = self.__robotCoord
        fullMap[row][col] = '🤖'

        numberIconString = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        print(f"\n########## 🗺️ {whichMap} Map: ##########")
        cols, rows = self.get_map_length()
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
