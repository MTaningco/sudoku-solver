class Line:
    def __init__(self, cells, sectionNumber, isRow):
        self.cells = cells
        self.sectionNumber = sectionNumber
        self.isRow = isRow

    def containsCell(self, row, col):
        if self.isRow:
            return self.sectionNumber == row
        else:
            return self.sectionNumber == col
