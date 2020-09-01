import collections


class Cell:
    # Constructs the Cell
    def __init__(self, row, col):
        self.__tuple = (row, col)
        self.__valList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Checks if the value is contained in the value list
    def contains(self, val):
        return val in self.__valList

    # Gets the column
    def getCol(self):
        return self.__tuple[1]

    # Gets the row
    def getRow(self):
        return self.__tuple[0]

    # Gets the value list
    def getValList(self):
        return self.__valList

    # Gets the size of the value list
    def getValListSize(self):
        return len(self.__valList)

    # Gets the value of the cell, ensuring that there is only one value left
    def getValue(self):
        if len(self.__valList) <= 0:
            raise Exception("Error trying to get value when cell has no possible solutions")
        elif len(self.__valList) > 1:
            raise Exception("Error trying to get value when the cell is not solved")
        else:
            return self.__valList[0]

    # Checks if cell has any possible solutions
    def hasNoSolution(self):
        return len(self.__valList) <= 0

    # Checks if the value lists are equivalent
    def isEqualsValList(self, otherValList):
        return collections.Counter(self.__valList) == collections.Counter(otherValList)

    # Checks if the cell is solved
    def isSolved(self):
        return len(self.__valList) == 1

    # Performs a set difference with the other list
    def removeElements(self, otherList):
        self.__valList = list(set(self.__valList) - set(otherList.__valList))

    # Removes the value from the list
    def removeVal(self, val):
        if val in self.__valList:
            self.__valList.remove(val)
            if len(self.__valList) <= 0:
                raise Exception("No possibilities left for cell({row}, {col})\n".format(row=self.__tuple[0], col=self.__tuple[1]))

    # Sets the value list
    def setValList(self, valList):
        self.__valList = valList

    # Sets the value list to just one value
    def setValue(self, val):
        self.__valList.clear()
        self.__valList.append(val)
