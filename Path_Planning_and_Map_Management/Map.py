from typing import List, Tuple
from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Data_Structures.Spot import Spot

class Map:
    def __init__(self):
        self.__mapLength: Tuple[int, int] = (0, 0)
        self.__robotCoord: Tuple[int, int, int] = (0, 0, 0)  # row, col, direction(북동남서 순으로 0~4)
        self.__spots: List[Spot] = []
        self.__hazards: List[Hazard] = []
        self.__colorBlobs: List[ColorBlob] = []
    
    #지도의 행과 열의 길이를 반환
    def getMapLength(self): 
        return self.__mapLength

    #지도의 행과 열의 길이를 설정
    def setMapLength(self, rows, cols):
        self.__mapLength = (rows, cols)
        
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

    # 새로운 위험 지점 추가
    def addHazard(self, hazard: Hazard):
        self.__hazards.append(hazard)

    # 새로운 중요 지점 추가
    def addColorBlob(self, colorBlob: ColorBlob):
        self.__colorBlobs.append(colorBlob)

    # 숨겨진 지점을 공개된 지점으로 변경
    def revealHidden(self, point: ColorBlob):
        if point is ColorBlob:
            for colorBlob in self.__colorBlobs:
                if point.position == colorBlob.position:
                    colorBlob.setRevealed()
        elif point is Hazard:
            for hazard in self.__hazards:
                if point.position == hazard.position:
                    hazard.setRevealed()

    # 전체 맵 반환 - 꼭 필요한 것인지 모르겠음. 일단 디버깅 위해 추가
    def getFullMap(self):
        # 맵의 크기에 맞는 2차원 배열 생성
        fullMap = [['⚪󠀠󠀠' for _ in range(self.__mapLength[1])] for _ in range(self.__mapLength[0])]
        
        # spots, hazards, colorBlobs를 맵에 표시
        for spot in self.__spots:  # '✅'는 방문한 탐색지점을 의미, '🎯'는 방문하지 않은 탐색지점
            r, c = spot.position
            fullMap[r][c] = '✅' if spot.isExplored() else '🎯'
        
        for hazard in self.__hazards:  # 'h'는 숨겨진 위험 지점을 의미, '⚠'는 공개된 위험 지점
            r, c = hazard.position
            fullMap[r][c] = 'hh' if hazard.isHidden() else '⚠️'
        
        for colorBlob in self.__colorBlobs:  # 'c'는 숨겨진 중요 지점을 의미, '🔵'는 공개된 중요 지점
            r, c = colorBlob.position
            fullMap[r][c] = 'cc' if colorBlob.isHidden() else '🔵'
        
        # 로봇의 위치를 맵에 표시
        r, c, d = self.__robotCoord
        fullMap[r][c] = '🤖'
        
        return fullMap