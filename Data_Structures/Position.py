from typing import Tuple


class Position:
    def __init__(self, col, row, visited=False, hidden=False):
        self.__position = (col, row)
        self.__visited = visited
        self.__hidden = hidden

    def setPosition(self, position: Tuple[int, int]):
        self.__position = position

    def getPosition(self):
        return self.__position

    def setVisited(self, visited: bool):
        self.__visited = visited

    def getVisited(self):
        return self.__visited

    def setHidden(self, hidden: bool):
        self.__hidden = hidden

    def getHidden(self):
        return self.__hidden
