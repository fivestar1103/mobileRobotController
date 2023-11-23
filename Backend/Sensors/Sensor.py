from typing import List, Tuple
from abc import ABC, abstractmethod


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
        raise NotImplementedError("Sensors must implement readSensor()")
