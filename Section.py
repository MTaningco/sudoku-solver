import collections
import copy

class Section:
    def __init__(self, cells):
        self.cells = cells
        # self.sectionRow = sectionRow
        # self.sectionColumn = sectionColumn

    # def containsCell(self, cell):
    #     # rowCheck = self.sectionRow * 3 <= row and (self.sectionRow + 1) * 3 > row
    #     # colCheck = self.sectionColumn * 3 <= col and (self.sectionColumn + 1) * 3 > col
    #     return cell in self.cells
    def __deepcopy__(self, memodict={}):
        return Section(copy.deepcopy(self.cells))

    def findError(self):
        for cell in self.cells:
            if len(cell.val) == 0:
                raise Exception("cell({row}, {col}) contains no possible solution".format(row=cell.tuple[0], col=cell.tuple[1]))
            elif len(cell.val) == 1:
                cellVal = cell.val[0]
                for probeCell in self.cells:
                    if probeCell is not cell and len(probeCell.val) == 1 and probeCell.val[0] == cellVal:
                        raise Exception("cell({row1}, {col1}) and cell({row2}, {col2}) contains the same value which is not possible".format(row1=cell.tuple[0], col1=cell.tuple[1], row2=probeCell.tuple[0], col2=probeCell.tuple[1]))

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

    def findCoupledSolution(self, cell, newSolvedQueue, oldSolvedQueue):
        # for every cell, find a n-1 different cell that has the n length and same numbers that is greater than or equal to two
            #once this is found, remove those numbers from the rest of the cells
        if len(newSolvedQueue) <= 0:
            for currentCell in self.cells:
                if len(currentCell.val) > 1:
                    totalNeeded = len(currentCell.val)
                    coupledCells = []
                    coupledCells.append(currentCell)
                    currentIndex = 0
                    while currentIndex < len(self.cells) and len(coupledCells) < totalNeeded:
                        if self.cells[currentIndex] is not currentCell and collections.Counter(currentCell.val) == collections.Counter(self.cells[currentIndex].val):
                            coupledCells.append(self.cells[currentIndex])
                        currentIndex += 1
                    if len(coupledCells) == totalNeeded:
                        # remove these numbers from all other cells
                        for complementaryCell in self.cells:
                            if complementaryCell not in coupledCells:
                                complementaryCell.val = list(set(complementaryCell.val) - set(coupledCells[0].val))

            for currentCell in self.cells:
                if currentCell.isSolved() and currentCell is not cell and currentCell not in newSolvedQueue and currentCell not in oldSolvedQueue:
                    newSolvedQueue.append(currentCell)
