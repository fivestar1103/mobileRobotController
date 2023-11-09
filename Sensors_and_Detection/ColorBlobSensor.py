from Sensors_and_Detection.Sensor import Sensor


class ColorBlobSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.setSensorType('C')

    # 주변 네 칸을 읽는다
    def readSensor(self, position):
        currentCol, currentRow = position[:2]
        newPositions = []
        for colDiff, rowDiff in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            newCol, newRow = currentCol + colDiff, currentRow + rowDiff
            newPosition = (newCol, newRow)
        newPositions.append(newPosition)
        self.setSensorData(newPositions)

    # 주변 네 칸이 중요 지점인지 판단
    def detectColorBlob(self, currentPosition, colorBlobs):
        self.readSensor(currentPosition)
        sensedPositions = self.getSensorData()

        revealedColorBlobs = []
        for colorBlob in colorBlobs:
            for sensedPosition in sensedPositions:
                if colorBlob.getPosition() == sensedPosition and colorBlob.isHidden():
                    revealedColorBlobs.append(colorBlob)

        return revealedColorBlobs
