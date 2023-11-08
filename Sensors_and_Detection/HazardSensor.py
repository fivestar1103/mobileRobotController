from Sensors_and_Detection.Sensor import Sensor


class HazardSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.setSensorType('H')

    # 바로 앞 칸을 읽는다
    def readSensor(self, position):
        currentRow, currentCol, currentDirection = position
        rowDiff, colDiff = [[1, 0], [0, 1], [-1, 0], [0, -1]][currentDirection]
        newRow, newCol = currentRow + rowDiff, currentCol + colDiff
        newPosition = (newRow, newCol)
        self.setSensorData([newPosition])

    # 바로 앞의 칸이 위험 지점인지 판단
    def detectHazard(self, currentPosition, hazards):
        self.readSensor(currentPosition)
        sensedPosition = self.getSensorData()[0]

        revealedHazards = []
        for hazard in hazards:
            if hazard.getPosition() == sensedPosition and hazard.isHidden():
                revealedHazards.append(hazard)

        return revealedHazards
