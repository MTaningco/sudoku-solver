class Cell:
    def __init__(self, row, col):
        self.tuple = (row, col)
        self.val = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def setValue(self, val):
        self.val.clear()
        self.val.append(val)

    def isSolved(self):
        return len(self.val) == 1

    def getValue(self):
        if len(self.val) > 1:
            return 0
        else:
            return self.val[0]

    def isEquals(self, row, col):
        return self.tuple[0] == row and self.tuple[1] == col

    def removeVal(self, val):
        if val in self.val:
            self.val.remove(val)
            if len(self.val) <= 0:
                print("error")
