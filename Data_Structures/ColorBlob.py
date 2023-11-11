from Data_Structures.Position import Position


class ColorBlob(Position):
    # ColorBlob의 status: hidden or revealed
    def __init__(self, col, row, hidden):
        super().__init__(col, row, status=hidden)

    def isHidden(self):
        return super().getStatus()

    def setRevealed(self):
        super().setStatus(False)
        print(f"[Robot]: 🔵ColorBlob at {self.getPosition()} was revealed!")

    def __str__(self):
        return f"ColorBlob({self.getPosition()}, Hidden: {self.isHidden()})"
