from board import *
import csv
import importlib as imp

with open('data/test.csv') as f:
	reader = csv.reader(f)
	sTraining = [row for row in reader]

# [print(x) for x in sTraining[1]]


sdk = SudokuSolver(TrainingBoard(sTraining[1]))
sdk.solve()
sdk.solution.print()
sdk.candidate.print(2)
sdk.update()
sdk.solution.print()

sdk.solve()
sdk.update()
sdk.candidate.print(2)
sdk.solution.print()

#run solve until candidate don't change