class Section:
    # Constructs the Sections
    def __init__(self, cells):
        self.cells = cells

    # Finds any errors in a section
    def find_error(self):
        for cell in self.cells:
            if cell.has_no_solution():
                raise Exception("Cell({row}, {col}) contains no possible solution".format(
                    row=cell.get_row(), col=cell.get_col()))
            elif cell.is_solved():
                cell_val = cell.get_value()
                for probeCell in self.cells:
                    if probeCell is not cell and probeCell.is_solved() and probeCell.get_value() == cell_val:
                        raise Exception("Cell({row1}, {col1}) and cell({row2}, {col2}) contains the same value which is"
                                        " not possible".format(row1=cell.get_row(), col1=cell.get_col(), row2=probeCell.
                                                               get_row(), col2=probeCell.get_col()))

    # Removes possible values from the section other than the cell of interest
    def remove_val_from_section_except(self, cell, new_solved_queue, old_solved_queue):
        if cell in self.cells:  # cell is present in the section
            for curCell in self.cells:  # go through every cell in the cells
                if curCell is not cell and curCell not in old_solved_queue and curCell not in new_solved_queue:
                    curCell.remove_val(cell.get_value())  # remove the value in that cell
                    if curCell.is_solved():
                        new_solved_queue.append(curCell)

    # Finds solutions that contains a unique number in only one cell
    def find_hidden_solution(self, cell, new_solved_queue, old_solved_queue):
        for curVal in range(1, 10):
            is_alone = True
            cell_of_interest = None
            for curCell in self.cells:
                if curCell.contains(curVal) and cell_of_interest is None:
                    cell_of_interest = curCell
                elif curCell.contains(curVal) and cell_of_interest is not None:
                    is_alone = False
                    break
            # cell of interest is not null, is_alone = True, set the value to be the number, add to solved queue
            if cell_of_interest is not None and is_alone and cell_of_interest is not cell and \
                    cell_of_interest not in old_solved_queue and cell_of_interest not in new_solved_queue:
                cell_of_interest.set_value(curVal)
                new_solved_queue.append(cell_of_interest)

    # Finds solutions by reducing the number of possibilities through coupling cells
    def find_coupled_solution(self, cell, new_solved_queue, old_solved_queue):
        if len(new_solved_queue) <= 0:
            for currentCell in self.cells:
                if not currentCell.is_solved() and not currentCell.has_no_solution():
                    total_needed = currentCell.get_val_list_size()
                    coupled_cells = [currentCell]
                    current_index = 0
                    while current_index < len(self.cells) and len(coupled_cells) < total_needed:
                        if self.cells[current_index] is not currentCell and currentCell.is_equals_val_list(
                                self.cells[current_index].get_val_list()):
                            coupled_cells.append(self.cells[current_index])
                        current_index += 1
                    if len(coupled_cells) == total_needed:
                        # remove these numbers from all other cells
                        for complementaryCell in self.cells:
                            if complementaryCell not in coupled_cells:
                                complementaryCell.remove_elements(coupled_cells[0])

            for currentCell in self.cells:
                if currentCell.is_solved() and currentCell is not cell and currentCell not in new_solved_queue and \
                        currentCell not in old_solved_queue:
                    new_solved_queue.append(currentCell)
