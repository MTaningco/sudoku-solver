from Cell import Cell
from Section import Section
import copy


class Board:
    # Constructs a board
    def __init__(self, jsonData):
        self.boardNum = 0
        self.array = []
        self.lowProbabilityCell = None
        self.newSolvedQueue = []
        self.oldSolvedQueue = []
        self.sections = []

        #populate cells onto the board
        for row in range(9):
            rowArray = []
            for col in range(9):
                rowArray.append(Cell(row, col))
            self.array.append(rowArray)

        #set initial conditions
        for jsonObj in jsonData:
            self.array[jsonObj['row']][jsonObj['column']].setValue(jsonObj['value'])
            self.newSolvedQueue.append(self.array[jsonObj['row']][jsonObj['column']])

        #setup sections
        for rowSection in range(3):
            for colSection in range(3):
                currentSection = []
                for actualRow in range(3):
                    for actualCol in range(3):
                        currentSection.append(self.array[rowSection * 3 + actualRow][colSection * 3 + actualCol])
                self.sections.append(Section(currentSection))
        for rowSection in range(9):
            currentSection = []
            for curCol in range(9):
                currentSection.append(self.array[rowSection][curCol])
            self.sections.append(Section(currentSection))
        for colSection in range(9):
            currentSection = []
            for curRow in range(9):
                currentSection.append(self.array[curRow][colSection])
            self.sections.append(Section(currentSection))

    # Deep copies a board
    def __deepcopy__(self, memodict={}):
        board = Board([])
        for row in board.array:
            for cell in row:
                cell.setValList(copy.deepcopy(self.array[cell.getRow()][cell.getCol()].getValList()))
        for cell in self.newSolvedQueue:
            board.newSolvedQueue.append(board.array[cell.getRow()][cell.getCol()])
        for cell in self.oldSolvedQueue:
            board.oldSolvedQueue.append(board.array[cell.getRow()][cell.getCol()])
        return board

    # Gets the value at the coordinate
    def __getValueAtCoordinate(self, row, col):
        isPretty = True
        if not isPretty:
            if self.array[row][col].isSolved():
                return str(self.array[row][col].getValue()) + " "*26
            else:
                return str(self.array[row][col].getValList()) + " " * 3 * (9 - self.array[row][col].getValListSize())
        else:
            if self.array[row][col].isSolved():
                return str(self.array[row][col].getValue())
            else:
                return '.'

    # Prints the board
    def printBoard(self):
        for rowSection in range(3):
            for row in range(3):
                print("", end=' ')
                for colSection in range(3):
                    for col in range(3):
                        print(self.__getValueAtCoordinate(rowSection * 3 + row, colSection*3 + col), end=' ')
                    if colSection < 2:
                        print("|", end=" ")
                print("")
            if rowSection < 2:
                print("-------+-------+-------")
        print("")

    # Solves the board through well defined logical steps
    def solve(self):
        while len(self.newSolvedQueue) > 0 and len(self.newSolvedQueue) + len(self.oldSolvedQueue) < 81:
            currentSolvedCell = self.newSolvedQueue.pop(0)
            self.oldSolvedQueue.append(currentSolvedCell)

            for section in self.sections:
                section.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.findCoupledSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.findError()

        if len(self.newSolvedQueue) + len(self.oldSolvedQueue) < 81:
            cellOfInterest = None
            valAmount = 10
            for row in self.array:
                for cell in row:
                    if not cell.isSolved() and not cell.hasNoSolution() and cell.getValListSize() < valAmount:
                        valAmount = cell.getValListSize()
                        cellOfInterest = cell
            self.lowProbabilityCell = cellOfInterest