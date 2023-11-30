from typing import Tuple


class Position:
    def __init__(self, col, row, status=False):
        self.__position = (col, row)
        self.__status = status

    def set_position(self, position: Tuple[int, int]):
        self.__position = position

    def get_position(self):
        return self.__position

    def set_status(self, status: bool):
        self.__status = status

    def get_status(self):
        return self.__status
