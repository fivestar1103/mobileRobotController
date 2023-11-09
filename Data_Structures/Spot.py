class Spot:
    def __init__(self, col, row, explored=False):
        self.position = (col, row)
        self.explored = explored

    def getPosition(self):
        return self.position

    def setExplored(self, explored):
        self.explored = explored
        if explored:
            print(f"✅ Spot at {self.getPosition()} was explored!")

    def isExplored(self):
        return self.explored

    def __str__(self):
        return f"Spot({self.position}, Explored: {self.explored})"
