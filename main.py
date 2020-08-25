import json
from Board import Board
from Cell import Cell

with open('test.json') as f:
  data = json.load(f)
# print(data)

# need to order json by row, column
board = Board(data['input'])
board.solve()

# cell1 = Cell(3, 3)
# cell1.setValue(3)
# cell2 = Cell(3, 4)
# cell2.setValue(4)
# cells = []
# cells.append(cell1)
# cells.append(cell2)
# print(cell1 in cells)

# a = [[0]*9]*9
# a = [[0]*9, [0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9]
# print(a)
# a[1][1] = 9
# print(a)