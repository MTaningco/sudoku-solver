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
    def get_col(self):
        return self.__tuple[1]

    # Gets the row
    def get_row(self):
        return self.__tuple[0]

    # Gets the value list
    def get_val_list(self):
        return self.__valList

    # Gets the size of the value list
    def get_val_list_size(self):
        return len(self.__valList)

    # Gets the value of the cell, ensuring that there is only one value left
    def get_value(self):
        if len(self.__valList) <= 0:
            raise Exception("Error trying to get value when cell has no possible solutions")
        elif len(self.__valList) > 1:
            raise Exception("Error trying to get value when the cell is not solved")
        else:
            return self.__valList[0]

    # Checks if cell has any possible solutions
    def has_no_solution(self):
        return len(self.__valList) <= 0

    # Checks if the value lists are equivalent
    def is_equals_val_list(self, other_val_list):
        return collections.Counter(self.__valList) == collections.Counter(other_val_list)

    # Checks if the cell is solved
    def is_solved(self):
        return len(self.__valList) == 1

    # Performs a set difference with the other list
    def remove_elements(self, other_list):
        self.__valList = list(set(self.__valList) - set(other_list.__valList))

    # Removes the value from the list
    def remove_val(self, val):
        if val in self.__valList:
            self.__valList.remove(val)
            if len(self.__valList) <= 0:
                raise Exception("No possibilities left for cell({row}, {col})\n".format(
                    row=self.__tuple[0], col=self.__tuple[1]))

    # Sets the value list
    def set_val_list(self, val_list):
        self.__valList = val_list

    # Sets the value list to just one value
    def set_value(self, val):
        self.__valList.clear()
        self.__valList.append(val)
