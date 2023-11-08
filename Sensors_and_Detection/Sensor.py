class Sensor:
    def __init__(self):
        self._sensorType = None
        self._sensorData = None

    def getSensorType(self):
        return self._sensorType

    def setSensorType(self, value):
        self._sensorType = value

    def getSensorData(self):
        return self._sensorData

    def setSensorData(self, value):
        self._sensorData = value

    def readSensor(self):
        raise NotImplementedError("Sensors must implement readSensor()")