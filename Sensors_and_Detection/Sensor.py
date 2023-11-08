from typing import List, Tuple


class Sensor:
    def __init__(self):
        self.__sensorType = None
        self.__sensorData = None

    def getSensorType(self):
        return self.__sensorType

    def setSensorType(self, value: str):  # H: Hazard, C: ColorBlob, P: Position
        if value not in ("H", "C", "P"):
            raise ValueError("value must be one of 'H', 'C', or 'P'")
        self.__sensorType = value

    def getSensorData(self):
        return self.__sensorData

    def setSensorData(self, value: List[Tuple]):
        self.__sensorData = value

    def readSensor(self, position: Tuple):
        raise NotImplementedError("Sensors must implement readSensor()")