class Spot:
    def __init__(self, col, row, explored=False):
        self.__position = (col, row)
        self.__explored = explored

    def getPosition(self):
        return self.__position

    def setExplored(self, explored):
        self.__explored = explored
        if explored:
            print(f"✅ Spot at {self.getPosition()} was explored!")

    def isExplored(self):
        return self.__explored

    def __str__(self):
        return f"Spot({self.__position}, Explored: {self.__explored})"
