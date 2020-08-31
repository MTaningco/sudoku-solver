from Cell import Cell
from Section import Section
import copy
class Board:
    def __init__(self, jsonData):
        self.boardNum = 0
        self.array = []
        for row in range(9):
            rowArray = []
            for col in range(9):
                rowArray.append(Cell(row, col))
            self.array.append(rowArray)
        self.newSolvedQueue = []
        self.oldSolvedQueue = []
        for jsonObj in jsonData:
            # print("{row}, {col}, {val}".format(row=jsonObj['row'], col=jsonObj['column'], val=jsonObj['value']))
            self.array[jsonObj['row']][jsonObj['column']].setValue(jsonObj['value'])
            self.newSolvedQueue.append(self.array[jsonObj['row']][jsonObj['column']])
        self.sections = []
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
        self.printBoard()

    def __deepcopy__(self, memodict={}):
        board = Board([])
        board.array = copy.deepcopy(self.array)
        board.newSolvedQueue = copy.deepcopy(self.newSolvedQueue)
        board.oldSolvedQueue = copy.deepcopy(self.oldSolvedQueue)
        board.sections = copy.deepcopy(self.sections)
        return board

    def getValueAtCoordinate(self, row, col):
        isPretty = True
        if not isPretty:
            if self.array[row][col].getValue() != 0:
                return str(self.array[row][col].getValue()) + " "*26
            else:
                return str(self.array[row][col].val) + " "*3*(9-len(self.array[row][col].val))
        else:
            if self.array[row][col].getValue() != 0:
                return str(self.array[row][col].getValue())
            else:
                return '.'

    def printBoard(self):
        print("board iteration: " + str(self.boardNum))
        if self.boardNum == 151:
            print("")
        self.boardNum += 1
        for rowSection in range(3):
            for row in range(3):
                print("", end=' ')
                for colSection in range(3):
                    for col in range(3):
                        print(self.getValueAtCoordinate(rowSection * 3 + row, colSection*3 + col), end=' ')
                    if colSection < 2:
                        print("|", end=" ")
                print("")
            if rowSection < 2:
                print("-------+-------+-------")
        print("")

    def solve(self):
        # squareSections = []
        # for rowSection in range(3):
        #     for colSection in range(3):
        #         currentSection = []
        #         for actualRow in range(3):
        #             for actualCol in range(3):
        #                 currentSection.append(self.array[rowSection * 3 + actualRow][colSection * 3 + actualCol])
        #         squareSections.append(Section(currentSection))

        # horizontalLines = []
        # for rowSection in range(9):
        #     currentSection = []
        #     for curCol in range(9):
        #         currentSection.append(self.array[rowSection][curCol])
        #     horizontalLines.append(Section(currentSection))

        # verticalLines = []
        # for colSection in range(9):
        #     currentSection = []
        #     for curRow in range(9):
        #         currentSection.append(self.array[curRow][colSection])
        #     verticalLines.append(Section(currentSection))

        # have set up squares, horizontal, and vertical

        happenedOnce = False

        while len(self.newSolvedQueue) > 0 or len(self.newSolvedQueue) + len(self.oldSolvedQueue) < 81:
            print("length of new solved queue is " + str(len(self.newSolvedQueue)))
            currentSolvedCell = self.newSolvedQueue.pop(0)
            self.oldSolvedQueue.append(currentSolvedCell)

            # updates the board with the currentSolvedCell
            for section in self.sections:
                section.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentSquareSection in squareSections:
            #     currentSquareSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentHorizontalSection in horizontalLines:
            #     currentHorizontalSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentVerticalSection in verticalLines:
            #     currentVerticalSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            self.printBoard()

            # updates the board with cells that have values by themselves
            for section in self.sections:
                section.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentSquareSection in squareSections:
            #     currentSquareSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentHorizontalSection in horizontalLines:
            #     currentHorizontalSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentVerticalSection in verticalLines:
            #     currentVerticalSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            self.printBoard()

            # look for coupled cells and update the rest of the cells
            for section in self.sections:
                section.findCoupledSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentSquareSection in squareSections:
            #     currentSquareSection.findCoupledSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentHorizontalSection in horizontalLines:
            #     currentHorizontalSection.findCoupledSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # for currentVerticalSection in verticalLines:
            #     currentVerticalSection.findCoupledSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)

            self.printBoard()

            for section in self.sections:
                section.findError()
            # for currentSquareSection in squareSections:
            #     currentSquareSection.findError()
            # for currentHorizontalSection in horizontalLines:
            #     currentHorizontalSection.findError()
            # for currentVerticalSection in verticalLines:
            #     currentVerticalSection.findError()

            if len(self.newSolvedQueue) == 0 and not happenedOnce:
                happenedOnce = True
                self.array[7][1].setValue(1)
                self.newSolvedQueue.append(self.array[7][1])
        print("asdf")