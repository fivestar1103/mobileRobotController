# 이 클래스는 SIM을 구현한 것으로, robot movement interface를 포함한다.
# 다음 기능을 수행한다:
# 로봇을 앞으로 한칸 이동시킨다
# 로봇을 시계방향으로 90도 회전시킨다
# 센서를 사용해 자신의 위치를 구한다
# 센서를 사용해 위험 지점을 찾는다
# 센서를 사용해 중요 지점을 찾는다

import random
from typing import List

from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Sensors_and_Detection.ColorBlobSensor import ColorBlobSensor
from Sensors_and_Detection.HazardSensor import HazardSensor
from Sensors_and_Detection.PositionSensor import PositionSensor


class RobotController:
    def __init__(self):
        self.__currentPosition = (0, 0, 0)  # 로봇의 현재 위치와 방향

    # 로봇의 현재 위치를 반환
    def getCurrentPosition(self):
        return self.__currentPosition

    # 로봇의 현재 위치를 설정
    def setCurrentPosition(self, position):
        self.__currentPosition = position

    # 로봇을 앞으로 한칸 전진시킨다
    def move(self, hazards, mapLength):
        prob = random.randint(1, 11)
        moveCount = 1 if prob > 3 else 2  # 30% 확률로 2칸 이동

        movementAccordingToDirection = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        currentCol, currentRow, currentDirection = self.getCurrentPosition()

        colDiff, rowDiff = movementAccordingToDirection[currentDirection]
        newCol, newRow = currentCol + colDiff * moveCount, currentRow + rowDiff * moveCount

        # 예외 설정
        isException = False
        # 2칸 앞이 hazard인 경우
        for hazard in hazards:
            if hazard.getPosition() == (newCol, newRow):
                isException = True
                break
        # 맵 밖으로 이동하는 경우
        if (newCol < 0 or newCol >= mapLength[0]) or (newRow < 0 or newRow >= mapLength[1]):
            isException = True
        if isException:
            moveCount = 1
            newCol, newRow = currentCol + colDiff * moveCount, currentRow + rowDiff * moveCount

        newPosition = (newCol, newRow, currentDirection)
        self.setCurrentPosition(newPosition)

        print(f"\tRobot has moved {moveCount} time(s) and now at {self.__currentPosition[:2]}")

    # 로봇을 시계방향으로 90도 회전시킨다
    def rotate(self):
        currentDirection = self.__currentPosition[2]
        newDirection = (currentDirection + 1) % 4
        col, row = self.__currentPosition[:2]
        self.setCurrentPosition((col, row, newDirection))

        directionDict = ['N', 'E', 'S', 'W']
        print(f"\tRobot has rotated and now facing {directionDict[self.__currentPosition[2]]}")

    # 센서를 통해 위험 지점 감지
    def detectHazard(self, hazards) -> Hazard:
        hazardSensor = HazardSensor()
        return hazardSensor.detectHazard(self.getCurrentPosition(), hazards)

    # 센서를 통해 중요 지점 감지
    def detectColorBlob(self, colorBlobs) -> List[ColorBlob]:
        colorBlobSensor = ColorBlobSensor()
        return colorBlobSensor.detectColorBlob(self.getCurrentPosition(), colorBlobs)

    # 센서를 통해 현재 위치 감지
    def detectPosition(self):
        positionSensor = PositionSensor()
        return positionSensor.detectPosition(self.getCurrentPosition())
