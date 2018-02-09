#ToDo Next:
	#do the pairs thing for rows and cols

	#should make this run tests..

	#memoize the solved ones

	#clean up code
		#do i need a sdk.solution class in the first place?


from board import *
from grids import *
import csv
import sys

# read from generated sudoku
def read():
	global sTraining
	with open('data/test.csv') as f:
		reader = csv.reader(f)
		sTraining = [row for row in reader]

def main(level='medium', date='all', _print=False ): #oneLoop=False -> to implement
	global sdk
	if level == 'e': 
		level = 'easy'
	elif level == 'h':
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
		main(input("level(easy, medium, hard): "),  input("date(mmdd, all, latest): "), input("print? (n = Enter): "))