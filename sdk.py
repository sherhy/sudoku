#ToDo Next:
	#memoize the solved ones ->
		#create interface that can dynamically store into data csv file

	#should make this run tests..

	#clean up code
		#do i need a sdk.solution class in the first place?

from board import *
from grids import *
import csv
import sys

# read from generated sudoku
def read():
	global sTraining
	sTraining = list()
	with open('data/test.csv') as f:
		reader = csv.reader(f)
		sTraining = [row for row in reader]


def main(level='medium', date='all', _print=False ): #oneLoop=False -> to implement
	global sdk
	if level == 'e' or level == 'easy': 
		level = 'easy'
	elif level == 'h' or level == 'hard':
		level = 'hard'
	else:
		level = 'medium'

	if date  == 'latest':  
		date = list(problemset[level]).pop()
	elif date.isnumeric():
		pass
	else: date = 'all'

	if date != 'all':
		print(level, date)
		sdk = SudokuSolver(TrainingBoard(problemset[level][date]))
		sdk.solve()

		if _print: sdk.print()
		print('no error:', sdk.solution.isLglSdk())
	else:
		success, error = 0,0
		for i in list(problemset[level]):
			print(level, i)
			sdk = SudokuSolver(TrainingBoard(problemset[level][i]))
			sdk.solve()
			if _print: sdk.print()

			if not sdk.solution.isLglSdk(): error +=1
			if sdk.solution.isLglSdk(1): success +=1
		total = len(problemset[level])
		print('final grade: {0}/{1}'.format(success, total), success/total*100, '%\nerrors:', error, end =" ")
		if not error: print("no errors, great!")
		else: print()

if __name__=="__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1], sys.argv[2], None if len(sys.argv) == 3 else sys.argv[3])
	else: 
		mode = input("mode ('macro' or 'single'): ")
		if mode == 'macro' or mode=='m':
			main(input("level(easy, medium, hard): "),  input("date(mmdd, all, latest): "), input("print? (n = Enter): "))
		
		grid = Board(_input=True)
		sdk = SudokuSolver(grid)

		sdk.solve()
		sdk.print()
		#sdk.save()

		quit("see you next time")