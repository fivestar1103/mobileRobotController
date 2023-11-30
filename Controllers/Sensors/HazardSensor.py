# 이 클래스는 로봇의 위험 지점 센서를 구현한 것이다.
# 바로 앞의 한칸을 탐색하여 위험 지점 여부를 판별한다.
# 숨겨진 위험지점이 발견되면 그 지점을 공개된 위험지점으로 바꾼다.

from Controllers.Sensors.Sensor import Sensor


class HazardSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.set_sensor_type('H')

    # 바로 앞 칸을 읽는다
    def read_sensor(self, position):
        currentCol, currentRow, currentDirection = position
        colDiff, rowDiff = [[0, 1], [1, 0], [0, -1], [-1, 0]][currentDirection]
        newCol, newRow = currentCol + colDiff, currentRow + rowDiff
        newPosition = (newCol, newRow)
        self.set_sensor_data([newPosition])

    # 바로 앞의 칸이 위험 지점인지 판단
    def detect_hazard(self, currentPosition, hazards):
        self.read_sensor(currentPosition)
        sensedPosition = self.get_sensor_data()[0]

        revealedHazard = None
        for hazard in hazards:
            if hazard.get_position() == sensedPosition and hazard.is_hidden():
                revealedHazard = hazard
                break

        return revealedHazard
