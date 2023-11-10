from Data_Structures.Position import Position


class ColorBlob(Position):
    def __init__(self, col, row, hidden=False):
        super().__init__(col, row, hidden=hidden)

    def isHidden(self):
        return super().getHidden()

    def setRevealed(self):
        super().setHidden(False)
        print(f"[Robot]: 🔵ColorBlob at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"ColorBlob({self.getPosition()}, Hidden: {self.isHidden()})"
