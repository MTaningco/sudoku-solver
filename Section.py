class Section:
    def __init__(self, cells):
        self.cells = cells
        # self.sectionRow = sectionRow
        # self.sectionColumn = sectionColumn

    # def containsCell(self, cell):
    #     # rowCheck = self.sectionRow * 3 <= row and (self.sectionRow + 1) * 3 > row
    #     # colCheck = self.sectionColumn * 3 <= col and (self.sectionColumn + 1) * 3 > col
    #     return cell in self.cells

    #assumes that contains cell was first used
    def removeValFromSectionExcept(self, cell, newSolvedQueue, oldSolvedQueue):
        if cell in self.cells:# cell is present in the section
            for curCell in self.cells:#go through every cell in the cells
                if curCell is not cell and curCell not in oldSolvedQueue and curCell not in newSolvedQueue:#the cell youre looking at is not the cell with the value you want to remove, and not an old solved thing, and not just added in the new solved thing
                    curCell.removeVal(cell.getValue())# remove the value in that cell
                    if curCell.isSolved():
                        print("cell added with the properties {row} {col} {val}".format(row=curCell.tuple[0], col=curCell.tuple[1], val=curCell.val[0]))
                        newSolvedQueue.append(curCell)

    def findHiddenSolution(self, cell, newSolvedQueue, oldSolvedQueue):
        for curVal in range(1, 10):
            isAlone = True
            cellOfInterest = None
            for curCell in self.cells:
                if curVal in curCell.val and cellOfInterest is None:
                    cellOfInterest = curCell
                elif curVal in curCell.val and cellOfInterest is not None:
                    isAlone = False
                    break
            # cell of interest is not null, isAlone = True, set the value to be the number, add to solved queue
            if cellOfInterest is not None and isAlone and cellOfInterest is not cell and cellOfInterest not in oldSolvedQueue and cellOfInterest not in newSolvedQueue:
                cellOfInterest.setValue(curVal)
                print("cell added with the properties {row} {col} {val}".format(row=cellOfInterest.tuple[0], col=cellOfInterest.tuple[1], val=cellOfInterest.val[0]))
                newSolvedQueue.append(cellOfInterest)

    def findCoupledSolution(self, newSolvedQueue):
        print("")
        # for every cell, find a n-1 different cell that has the n length and same numbers that is greater than or equal to two
            #once this is found, remove those numbers from the rest of the cells