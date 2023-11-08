class ColorBlob:
    def __init__(self, row, col, hidden=True):
        self.position = (row, col)
        self.hidden = hidden

    def getPosition(self):
        return self.position

    def isHidden(self):
        return self.hidden

    def setRevealed(self):
        self.hidden = False

    def __str__(self):
        return f"ColorBlob({self.position}, Hidden: {self.hidden})"
