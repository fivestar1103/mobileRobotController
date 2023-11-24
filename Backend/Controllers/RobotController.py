# 이 클래스는 SIM을 구현한 것으로, robot movement interface를 포함한다.
# 다음 기능을 수행한다:
# - 로봇을 앞으로 한칸 이동시킨다
# - 로봇을 시계방향으로 90도 회전시킨다
# - 센서를 사용해 자신의 위치를 구한다
# - 센서를 사용해 중요 지점을 찾는다
# - 센서를 사용해 위험 지점을 찾는다

import random
from typing import List

from Backend.Data_Structures.ColorBlob import ColorBlob
from Backend.Data_Structures.Hazard import Hazard
from Backend.Sensors.ColorBlobSensor import ColorBlobSensor
from Backend.Sensors.HazardSensor import HazardSensor
from Backend.Sensors.PositionSensor import PositionSensor


class RobotController:
    def __init__(self):
        self.__currentPosition = (0, 0, 0)  # 로봇의 현재 위치와 방향

    def get_current_position(self):  # 로봇의 현재 위치를 반환
        return self.__currentPosition

    def set_current_position(self, position):  # 로봇의 현재 위치를 설정
        self.__currentPosition = position

    def move(self, hazards, mapLength):  # 로봇을 앞으로 한칸 전진시킨다
        prob = random.randint(1, 11)
        moveCount = 1 if prob > 1 else 2  # 10% 확률로 2칸 이동

        movementAccordingToDirection = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        currentCol, currentRow, currentDirection = self.get_current_position()

        colDiff, rowDiff = movementAccordingToDirection[currentDirection]
        newCol, newRow = currentCol + colDiff * moveCount, currentRow + rowDiff * moveCount

        # 예외 설정
        isException = False
        # 2칸 앞이 hazard인 경우
        for hazard in hazards:
            if hazard.get_position() == (newCol, newRow):
                isException = True
                break
        # 맵 밖으로 이동하는 경우
        if (newCol < 0 or newCol >= mapLength[0]) or (newRow < 0 or newRow >= mapLength[1]):
            isException = True
        if isException:
            moveCount = 1
            newCol, newRow = currentCol + colDiff * moveCount, currentRow + rowDiff * moveCount

        newPosition = (newCol, newRow, currentDirection)
        self.set_current_position(newPosition)

        print(f"\tRobot has moved {moveCount} time(s) and now at {self.__currentPosition[:2]}")

    def rotate(self):  # 로봇을 시계방향으로 90도 회전시킨다
        currentDirection = self.__currentPosition[2]
        newDirection = (currentDirection + 1) % 4
        col, row = self.__currentPosition[:2]
        self.set_current_position((col, row, newDirection))

        directionDict = ['N', 'E', 'S', 'W']
        print(f"\tRobot has rotated and now facing {directionDict[self.__currentPosition[2]]}")

    def detect_hazard(self, hazards) -> Hazard:  # 센서를 통해 위험 지점 감지
        hazardSensor = HazardSensor()
        return hazardSensor.detect_hazard(self.get_current_position(), hazards)

    def detect_color_blob(self, colorBlobs) -> List[ColorBlob]:  # 센서를 통해 중요 지점 감지
        colorBlobSensor = ColorBlobSensor()
        return colorBlobSensor.detect_color_blob(self.get_current_position(), colorBlobs)

    def detect_position(self):  # 센서를 통해 현재 위치 감지
        positionSensor = PositionSensor()
        return positionSensor.detect_position(self.get_current_position())
