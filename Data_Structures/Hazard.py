from Data_Structures.Position import Position


class Hazard(Position):
    # Hazard의 status: hidden or revealed
    def __init__(self, col, row, hidden):
        super().__init__(col, row, status=hidden)

    def isHidden(self):
        return super().getStatus()

    def setRevealed(self):
        super().setStatus(False)
        print(f"[Robot]: ⚠️Hazard at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"Hazard({self.getPosition()}, Hidden: {self.isHidden()})"
