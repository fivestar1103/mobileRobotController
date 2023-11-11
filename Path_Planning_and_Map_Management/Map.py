from typing import List, Tuple
from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Data_Structures.Spot import Spot


class Map:
    def __init__(self):
        self.__mapLength: Tuple[int, int] = (0, 0)
        self.__robotCoord: Tuple[int, int, int] = (0, 0, 0)  # col, row, direction(북동남서 순으로 0~4)
        self.__spots: List[Spot] = []
        self.__hazards: List[Hazard] = []
        self.__colorBlobs: List[ColorBlob] = []

    #지도의 행과 열의 길이를 반환
    def getMapLength(self):
        return self.__mapLength

    #지도의 행과 열의 길이를 설정
    def setMapLength(self, cols, rows):
        self.__mapLength = (cols, rows)

    #로봇의 위치 반환
    def getRobotCoord(self):
        return self.__robotCoord

    def setRobotCoord(self, position: (int, int, int)):
        self.__robotCoord = position

    #모든 탐색 지점을 반환
    def getSpots(self):
        return self.__spots

    #탐색 지점들을 설정
    def setSpots(self, spots: List[Spot]):
        self.__spots = spots

    # 모든 위험 지점을 반환
    def getHazards(self):
        return self.__hazards

    # 위험 지점들을 생성
    def setHazards(self, hazards: List[Hazard]):
        self.__hazards = hazards

    # 모든 중요 지점을 반환
    def getColorBlobs(self):
        return self.__colorBlobs

    # 중요 지점을 설정
    def setColorBlobs(self, colorBlobs: List[ColorBlob]):
        self.__colorBlobs = colorBlobs

    # 새로운 지점 추가
    def addNewPoints(self, newPoints: List):
        newPointCount = 0
        for newPoint in newPoints:
            if type(newPoint) is Hazard:
                if not any(hazard.getPosition() == newPoint.getPosition() for hazard in self.getHazards()):
                    self.__hazards.append(newPoint)
                    newPointCount += 1
            elif type(newPoint) is ColorBlob:
                if not any(colorBlob.getPosition() == newPoint.getPosition() for colorBlob in self.getColorBlobs()):
                    self.__colorBlobs.append(newPoint)
                    newPointCount += 1
            elif type(newPoint) is Spot:
                if not any(spot.getPosition() == newPoint.getPosition() for spot in self.getSpots()):
                    self.__spots.append(newPoint)
                    newPointCount += 1
        print(f"\t{newPointCount} new points have been added...")

    # 숨겨진 지점을 공개된 지점으로 변경
    def revealHidden(self, point):
        if type(point) == ColorBlob:
            for colorBlob in self.__colorBlobs:
                if point.getPosition() == colorBlob.getPosition():
                    colorBlob.setRevealed()
        elif type(point) == Hazard:
            for hazard in self.__hazards:
                if point.getPosition() == hazard.getPosition():
                    hazard.setRevealed()

    # 전체 맵 반환 - 꼭 필요한 것인지 모르겠음. 일단 디버깅 위해 추가
    def printFullMap(self, whichMap=''):
        # 맵의 크기에 맞는 2차원 배열 생성
        cols, rows = self.getMapLength()
        fullMap = [['⚪󠀠󠀠' for _ in range(cols)] for _ in range(rows)]

        # spots, hazards, colorBlobs를 맵에 표시
        for spot in self.__spots:  # '✅'는 방문한 탐색지점을 의미, '🎯'는 방문하지 않은 탐색지점
            col, row = spot.getPosition()
            fullMap[row][col] = '✅' if spot.isExplored() else '🎯'

        for hazard in self.__hazards:  # 'h'는 숨겨진 위험 지점을 의미, '⚠'는 공개된 위험 지점
            col, row = hazard.getPosition()
            fullMap[row][col] = 'hh' if hazard.isHidden() else '⚠️'

        for colorBlob in self.__colorBlobs:  # 'c'는 숨겨진 중요 지점을 의미, '🔵'는 공개된 중요 지점
            col, row = colorBlob.getPosition()
            fullMap[row][col] = 'cc' if colorBlob.isHidden() else '🔵'

        # 로봇의 위치를 맵에 표시
        col, row, direction = self.__robotCoord
        fullMap[row][col] = '🤖'

        numberIconString = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        print(f"\n########## 🗺️ {whichMap} Map: ##########")
        cols, rows = self.getMapLength()
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
