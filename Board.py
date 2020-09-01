from Cell import Cell
from Section import Section
import copy


class Board:
    # Constructs a board
    def __init__(self, json_data):
        self.boardNum = 0
        self.array = []
        self.lowProbabilityCell = None
        self.newSolvedQueue = []
        self.oldSolvedQueue = []
        self.sections = []

        # Populate cells onto the board
        for row in range(9):
            row_array = []
            for col in range(9):
                row_array.append(Cell(row, col))
            self.array.append(row_array)

        # Set initial conditions
        for jsonObj in json_data:
            self.array[jsonObj['row']][jsonObj['column']].set_value(jsonObj['value'])
            self.newSolvedQueue.append(self.array[jsonObj['row']][jsonObj['column']])

        # Setup sections
        for rowSection in range(3):
            for colSection in range(3):
                current_section = []
                for actualRow in range(3):
                    for actualCol in range(3):
                        current_section.append(self.array[rowSection * 3 + actualRow][colSection * 3 + actualCol])
                self.sections.append(Section(current_section))
        for rowSection in range(9):
            current_section = []
            for curCol in range(9):
                current_section.append(self.array[rowSection][curCol])
            self.sections.append(Section(current_section))
        for colSection in range(9):
            current_section = []
            for curRow in range(9):
                current_section.append(self.array[curRow][colSection])
            self.sections.append(Section(current_section))

    # Deep copies a board
    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        board = Board([])
        for row in board.array:
            for cell in row:
                cell.set_val_list(copy.deepcopy(self.array[cell.get_row()][cell.get_col()].get_val_list()))
        for cell in self.newSolvedQueue:
            board.newSolvedQueue.append(board.array[cell.get_row()][cell.get_col()])
        for cell in self.oldSolvedQueue:
            board.oldSolvedQueue.append(board.array[cell.get_row()][cell.get_col()])
        return board

    # Gets the value at the coordinate
    def __get_value_at_coordinate(self, row, col):
        is_pretty = True
        if not is_pretty:
            if self.array[row][col].is_solved():
                return str(self.array[row][col].get_value()) + " " * 26
            else:
                return str(self.array[row][col].get_val_list()) + " " * 3 * \
                       (9 - self.array[row][col].get_val_list_size())
        else:
            if self.array[row][col].is_solved():
                return str(self.array[row][col].get_value())
            else:
                return '.'

    # Prints the board
    def print_board(self):
        for rowSection in range(3):
            for row in range(3):
                print("", end=' ')
                for colSection in range(3):
                    for col in range(3):
                        print(self.__get_value_at_coordinate(rowSection * 3 + row, colSection * 3 + col), end=' ')
                    if colSection < 2:
                        print("|", end=" ")
                print("")
            if rowSection < 2:
                print("-------+-------+-------")
        print("")

    # Solves the board through well defined logical steps
    def solve(self):
        while len(self.newSolvedQueue) > 0 and len(self.newSolvedQueue) + len(self.oldSolvedQueue) < 81:
            current_solved_cell = self.newSolvedQueue.pop(0)
            self.oldSolvedQueue.append(current_solved_cell)

            for section in self.sections:
                section.remove_val_from_section_except(current_solved_cell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.find_hidden_solution(current_solved_cell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.find_coupled_solution(current_solved_cell, self.newSolvedQueue, self.oldSolvedQueue)

            for section in self.sections:
                section.find_error()

        if len(self.newSolvedQueue) + len(self.oldSolvedQueue) < 81:
            cell_of_interest = None
            val_amount = 10
            for row in self.array:
                for cell in row:
                    if not cell.is_solved() and not cell.has_no_solution() and cell.get_val_list_size() < val_amount:
                        val_amount = cell.get_val_list_size()
                        cell_of_interest = cell
            self.lowProbabilityCell = cell_of_interest
