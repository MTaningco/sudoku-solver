from Cell import Cell
from Section import Section
from Line import Line
class Board:
    def __init__(self, jsonData):
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
        self.printBoard()

    def getValueAtCoordinate(self, row, col):
        isPretty = False
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
        squareSections = []
        for rowSection in range(3):
            for colSection in range(3):
                currentSection = []
                for actualRow in range(3):
                    for actualCol in range(3):
                        currentSection.append(self.array[rowSection * 3 + actualRow][colSection * 3 + actualCol])
                squareSections.append(Section(currentSection))

        horizontalLines = []
        for rowSection in range(9):
            currentSection = []
            for curCol in range(9):
                currentSection.append(self.array[rowSection][curCol])
            horizontalLines.append(Section(currentSection))

        verticalLines = []
        for colSection in range(9):
            currentSection = []
            for curRow in range(9):
                currentSection.append(self.array[curRow][colSection])
            verticalLines.append(Section(currentSection))

        # have set up squares, horizontal, and vertical

        while len(self.newSolvedQueue) > 0:
            currentSolvedCell = self.newSolvedQueue.pop(0)
            # remove
            # print("starting on square section removal phase")
            for currentSquareSection in squareSections:
                currentSquareSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # print("starting on horizontal section removal phase")
            for currentHorizontalSection in horizontalLines:
                currentHorizontalSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # print("starting on vertical section removal phase")
            for currentVerticalSection in verticalLines:
                currentVerticalSection.removeValFromSectionExcept(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            #at this point, done eliminating the cell from every cell in its section, the newsolved queue mightve added another solved cell in there, still need to check for hidden solutions
            # see if you can find hidden solutions
            # print("starting on square section hidden phase")
            for currentSquareSection in squareSections:
                currentSquareSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # print("starting on horizontal section hidden phase")
            for currentHorizontalSection in horizontalLines:
                currentHorizontalSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            # print("starting on vertical section hidden phase")
            for currentVerticalSection in verticalLines:
                currentVerticalSection.findHiddenSolution(currentSolvedCell, self.newSolvedQueue, self.oldSolvedQueue)
            self.oldSolvedQueue.append(currentSolvedCell)
            self.printBoard()
            if len(self.newSolvedQueue) == 0:
                print("asdf")
                # find coupled groups, size 2 for both cells, same 2 numbers, size 3 for 3 cells, same 3 numbers, etc?
        print("asdf")