from Sensors_and_Detection.Sensor import Sensor


class PositionSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.setSensorType('P')

    # 로봇의 실제 위치를 읽는다
    def readSensor(self, position):
        currentCol, currentRow, currentDirection = position
        sensedCol, sensedRow = currentCol - 0, currentRow - 0
        sensedPosition = [(sensedCol, sensedRow, currentDirection)]
        self.setSensorData(sensedPosition)

    # 로봇의 실제 위치가 SIM 위치와 같은지 확인한다
    def detectPosition(self, actualPosition):
        self.readSensor(actualPosition)
        sensedPosition = self.getSensorData()[0]
        robotPosition = sensedPosition
        return robotPosition
