class Hazard:
    def __init__(self, col, row, hidden=True):
        self.__position = (col, row)
        self.__hidden = hidden

    def getPosition(self):
        return self.__position

    def isHidden(self):
        return self.__hidden

    def setRevealed(self):
        self.__hidden = False
        print(f"⚠️ Hazard at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"Hazard({self.__position}, Hidden: {self.__hidden})"
