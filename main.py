import json
from Board import Board
import copy


# Recursively solves the board
def recursive_solve(board, board_id):
    try:
        print("Board version {id} initial state".format(id=board_id))
        board.print_board()
        board.solve()
        print("Board version {id} final state".format(id=board_id))
        board.print_board()
        if board.lowProbabilityCell is not None:
            cell = board.lowProbabilityCell
            id_offset = 0
            for possibleVal in cell.get_val_list():
                print("Split board {id} with cell({row}, {col}) = {val}".format(id=board_id, row=cell.get_row(),
                                                                                col=cell.get_col(), val=possibleVal))
                possible_board = copy.deepcopy(board)
                possible_board.array[cell.get_row()][cell.get_col()].set_value(possibleVal)
                possible_board.newSolvedQueue.append(possible_board.array[cell.get_row()][cell.get_col()])

                try:
                    return recursive_solve(possible_board, board_id + str(id_offset))
                except Exception as recursive_err:
                    print(recursive_err)
                    id_offset += 1
                    continue
            raise Exception("All possibilities contain no valid solution")
        else:
            return board
    except Exception as base_err:
        raise Exception("{err}\nBoard cannot contains error... Abort {id}".format(err=base_err, id=board_id))


with open('test.json') as f:
    data = json.load(f)

try:
    solved_board = recursive_solve(Board(data['input']), "0")
    print("Final solution")
    solved_board.print_board()
except Exception as e:
    print(e)
    print("Board has no solution")
