class Section:
    # Constructs the Sections
    def __init__(self, cells):
        self.cells = cells

    # Finds any errors in a section
    def findError(self):
        for cell in self.cells:
            if cell.hasNoSolution():
                raise Exception("Cell({row}, {col}) contains no possible solution".format(row=cell.getRow(), col=cell.getCol()))
            elif cell.isSolved():
                cellVal = cell.getValue()
                for probeCell in self.cells:
                    if probeCell is not cell and probeCell.isSolved() and probeCell.getValue() == cellVal:
                        raise Exception("Cell({row1}, {col1}) and cell({row2}, {col2}) contains the same value which is not possible".format(row1=cell.getRow(), col1=cell.getCol(), row2=probeCell.getRow(), col2=probeCell.getCol()))

    # Removes possible values from the section other than the cell of interest
    def removeValFromSectionExcept(self, cell, newSolvedQueue, oldSolvedQueue):
        if cell in self.cells:# cell is present in the section
            for curCell in self.cells:#go through every cell in the cells
                if curCell is not cell and curCell not in oldSolvedQueue and curCell not in newSolvedQueue:#the cell youre looking at is not the cell with the value you want to remove, and not an old solved thing, and not just added in the new solved thing
                    curCell.removeVal(cell.getValue())# remove the value in that cell
                    if curCell.isSolved():
                        newSolvedQueue.append(curCell)

    # Finds solutions that contains a unique number in only one cell
    def findHiddenSolution(self, cell, newSolvedQueue, oldSolvedQueue):
        for curVal in range(1, 10):
            isAlone = True
            cellOfInterest = None
            for curCell in self.cells:
                if curCell.contains(curVal) and cellOfInterest is None:
                    cellOfInterest = curCell
                elif curCell.contains(curVal) and cellOfInterest is not None:
                    isAlone = False
                    break
            # cell of interest is not null, isAlone = True, set the value to be the number, add to solved queue
            if cellOfInterest is not None and isAlone and cellOfInterest is not cell and cellOfInterest not in oldSolvedQueue and cellOfInterest not in newSolvedQueue:
                cellOfInterest.setValue(curVal)
                # print("cell added with the properties {row} {col} {val}".format(row=cellOfInterest.tuple[0], col=cellOfInterest.tuple[1], val=cellOfInterest.val[0]))
                newSolvedQueue.append(cellOfInterest)

    # Finds solutions by reducing the number of possibilities through coupling cells
    def findCoupledSolution(self, cell, newSolvedQueue, oldSolvedQueue):
        # for every cell, find a n-1 different cell that has the n length and same numbers that is greater than or equal to two
            #once this is found, remove those numbers from the rest of the cells
        if len(newSolvedQueue) <= 0:
            for currentCell in self.cells:
                if not currentCell.isSolved() and not currentCell.hasNoSolution():
                    totalNeeded = currentCell.getValListSize()
                    coupledCells = []
                    coupledCells.append(currentCell)
                    currentIndex = 0
                    while currentIndex < len(self.cells) and len(coupledCells) < totalNeeded:
                        if self.cells[currentIndex] is not currentCell and currentCell.isEqualsValList(self.cells[currentIndex].getValList()):
                            coupledCells.append(self.cells[currentIndex])
                        currentIndex += 1
                    if len(coupledCells) == totalNeeded:
                        # remove these numbers from all other cells
                        for complementaryCell in self.cells:
                            if complementaryCell not in coupledCells:
                                complementaryCell.removeElements(coupledCells[0])

            for currentCell in self.cells:
                if currentCell.isSolved() and currentCell is not cell and currentCell not in newSolvedQueue and currentCell not in oldSolvedQueue:
                    newSolvedQueue.append(currentCell)
