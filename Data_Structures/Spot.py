from Data_Structures.Position import Position


class Spot(Position):
    def __init__(self, col, row, explored=False):
        super().__init__(col, row, visited=explored)

    def isExplored(self):
        return super().getVisited()

    def setExplored(self):
        super().setVisited(True)
        print(f"[Robot]: ✅Spot at {self.getPosition()} was explored!")

    def __str__(self):
        return f"Spot({self.getPosition()}, Explored: {self.isExplored()})"
