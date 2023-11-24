# 이 클래스는 로봇의 센서들의 부모 클래스를 구현한 추상 클래스이다.
# 센서 종류와 센서의 값을 담고 있다.
# 이 클래스를 상속하는 자식 클래스는 반드시 read_sensor 메서드를 오버라이딩 해야 한다.

from typing import List, Tuple
from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self):
        self.__sensorType = None
        self.__sensorData = None

    # 센서 타입을 반환
    def get_sensor_type(self):
        return self.__sensorType

    # 센서 타입을 설정
    def set_sensor_type(self, value: str):  # H: Hazard, C: ColorBlob, P: Position
        if value not in ("H", "C", "P"):
            raise ValueError("value must be one of 'H', 'C', or 'P'")
        self.__sensorType = value

    # 센서 값을 반환
    def get_sensor_data(self):
        return self.__sensorData

    # 센서 값을 설정
    def set_sensor_data(self, value: List[Tuple]):
        self.__sensorData = value

    # 센서 값을 읽는 추상 클래스. 자식 클래스는 반드시 오버라이딩 필요.
    @abstractmethod
    def read_sensor(self, position: Tuple):
        raise NotImplementedError("Sensors must implement readSensor()")
