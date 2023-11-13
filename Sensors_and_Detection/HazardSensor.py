from Sensors_and_Detection.Sensor import Sensor


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
