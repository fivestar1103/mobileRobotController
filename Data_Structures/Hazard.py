class Hazard:
    def __init__(self, col, row, hidden=True):
        self.position = (col, row)
        self.hidden = hidden

    def getPosition(self):
        return self.position

    def isHidden(self):
        return self.hidden

    def setRevealed(self):
        self.hidden = False
        print(f"⚠️ Hazard at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"Hazard({self.position}, Hidden: {self.hidden})"
