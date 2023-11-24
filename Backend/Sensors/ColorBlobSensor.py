# 이 클래스는 로봇의 중요 지점 센서를 구현한 것이다.
# 상하좌우 한칸씩을 탐색하여 중요 지점 여부를 판별한다.
# 숨겨진 중요지점이 발견되면 그 지점을 공개된 중요지점으로 바꾼다.

from Backend.Sensors.Sensor import Sensor


class ColorBlobSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.set_sensor_type('C')

    # 주변 네 칸을 읽는다
    def read_sensor(self, position):
        currentCol, currentRow = position[:2]
        newPositions = []
        for colDiff, rowDiff in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            newCol, newRow = currentCol + colDiff, currentRow + rowDiff
            newPosition = (newCol, newRow)
            newPositions.append(newPosition)
        self.set_sensor_data(newPositions)

    # 주변 네 칸이 중요 지점인지 판단
    def detect_color_blob(self, currentPosition, colorBlobs):
        self.read_sensor(currentPosition)
        sensedPositions = self.get_sensor_data()

        revealedColorBlobs = []
        hiddenColorBlobs = [colorBlob for colorBlob in colorBlobs if colorBlob.is_hidden()]
        for hiddenColorBlob in hiddenColorBlobs:
            if hiddenColorBlob.get_position() in sensedPositions:
                revealedColorBlobs.append(hiddenColorBlob)

        return revealedColorBlobs
