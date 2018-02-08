from board import *
from grids import *
import csv
import importlib as imp

with open('data/test.csv') as f:
	reader = csv.reader(f)
	sTraining = [row for row in reader]

# sdk = SudokuSolver(TrainingBoard(sTraining[1]))
sdk = SudokuSolver(TrainingBoard(easy['0205']))
sdk.solve()
sdk.solution.print()

# while True:
# 	ans = input('go? ')
# 	if ans == 'n': break
# 	sdk.oneLoop()

print('islglSdk()',sdk.solution.isLglSdk())
print('sudoku_complete()', sdk.solution.isLglSdk(1))