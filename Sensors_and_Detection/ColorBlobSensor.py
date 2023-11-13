from Sensors_and_Detection.Sensor import Sensor


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
