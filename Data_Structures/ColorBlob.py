class ColorBlob:
    def __init__(self, col, row, hidden=True):
        self.__position = (col, row)
        self.hidden = hidden

    def getPosition(self):
        return self.position

    def isHidden(self):
        return self.hidden

    def setRevealed(self):
        self.hidden = False
        print(f"🔵 ColorBlob at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"ColorBlob({self.position}, Hidden: {self.hidden})"
