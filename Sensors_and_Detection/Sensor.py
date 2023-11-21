from abc import ABC, abstractmethod
from typing import Tuple, List


class Sensor(ABC):
    def __init__(self):
        self.__sensorType = None
        self.__sensorData = None

    def get_sensor_type(self):
        return self.__sensorType

    def set_sensor_type(self, value: str):  # H: Hazard, C: ColorBlob, P: Position
        if value not in ("H", "C", "P"):
            raise ValueError("value must be one of 'H', 'C', or 'P'")
        self.__sensorType = value

    def get_sensor_data(self):
        return self.__sensorData

    def set_sensor_data(self, value: List[Tuple]):
        self.__sensorData = value

    @abstractmethod
    def read_sensor(self, position: Tuple):
        """
        Derived sensor classes should implement this method to read sensor data
        based on the given position.
        """
        pass
