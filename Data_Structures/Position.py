from typing import Tuple


class Position:
    def __init__(self, col, row, status=False):
        self.__position = (col, row)
        self.__status = status

    def setPosition(self, position: Tuple[int, int]):
        self.__position = position

    def getPosition(self):
        return self.__position

    def setStatus(self, status: bool):
        self.__status = status

    def getStatus(self):
        return self.__status
