import json
from Board import Board
import copy


# Recursively solves the board
def recursiveSolve(board, id):
    try:
        print("Board version {id} initial state".format(id=id))
        board.printBoard()
        board.solve()
        print("Board version {id} final state".format(id=id))
        board.printBoard()
        if board.lowProbabilityCell is not None:
            cell = board.lowProbabilityCell
            idOffset = 0
            for possibleVal in cell.getValList():
                print("Split board {id} with cell({row}, {col}) = {val}".format(id=id, row=cell.getRow(), col=cell.getCol(), val=possibleVal))
                possibleBoard = copy.deepcopy(board)
                possibleBoard.array[cell.getRow()][cell.getCol()].setValue(possibleVal)
                possibleBoard.newSolvedQueue.append(possibleBoard.array[cell.getRow()][cell.getCol()])

                try:
                    return recursiveSolve(possibleBoard, id + str(idOffset))
                except Exception as e:
                    print(e)
                    idOffset += 1
                    continue
            raise Exception("All possibilities contain no valid solution")
        else:
            return board
    except Exception as e:
        raise Exception("{err}\nBoard cannot contains error... Abort {id}".format(err=e, id=id))


with open('test.json') as f:
    data = json.load(f)

try:
    board = recursiveSolve(Board(data['input']), "0")
    print("Final solution")
    board.printBoard()
except Exception as e:
    print(e)
    print("Board has no solution")
