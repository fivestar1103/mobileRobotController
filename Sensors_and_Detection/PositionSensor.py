from Sensors_and_Detection.Sensor import Sensor


class PositionSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.set_sensor_type('P')

    # 로봇의 실제 위치를 읽는다
    def read_sensor(self, position):
        currentCol, currentRow, currentDirection = position
        sensedCol, sensedRow = currentCol - 0, currentRow - 0
        sensedPosition = [(sensedCol, sensedRow, currentDirection)]
        self.set_sensor_data(sensedPosition)

    # 로봇의 실제 위치가 SIM 위치와 같은지 확인한다
    def detect_position(self, actualPosition):
        self.read_sensor(actualPosition)
        sensedPosition = self.get_sensor_data()[0]
        robotPosition = sensedPosition
        return robotPosition
