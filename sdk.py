#ToDo Next:
	#memoize the solved ones ->
		#or a save function for the answers

	#clean up code
		#do i need a sdk.solution class in the first place?

from board import *
# from grids import *
import csv, sys

# read from generated sudoku
def read(_level):
	with open('data/'+_level+'.csv') as f:
		reader = csv.reader(f)
		boards = [row for row in reader]
	return boards

def save(_level, _date, sdk):
	board = [str(item) for layer in sdk.puzzle for item in layer]
	board = ''.join(board)
	with open('data/'+_level+'.csv', 'a') as f:
		f.write('\n'+_date+','+board)

def main(level='medium', date='all', _print=False ): #oneLoop=False -> to implement
	if level == 'e' or level == 'easy': 
		level = 'easy'
	elif level == 'h' or level == 'hard':
		level = 'hard'
	else:
		level = 'medium'

	if date  == 'latest':  
		date = read(level)[-1][0]
	elif date.isnumeric():
		pass
	else: date = 'all'

	if date != 'all':
		board = list(filter(lambda x: x[0] == date, read(level)))[0]
		print(level, board[0])
		
		sdk = SudokuSolver(TrainingBoard(board))
		sdk.solve()

		if _print: sdk.print()
		print('no error:', sdk.solution.isLglSdk())
	else:
		success, error = 0,0
		boards = read(level)[1:]
		for board in boards:
			print(level, board[0])
			sdk = SudokuSolver(TrainingBoard(board))
			sdk.solve()
			if _print: sdk.print()

			if not sdk.solution.isLglSdk(): error +=1
			if sdk.solution.isLglSdk(1): success +=1
		total = len(boards)
		print('final grade: {0}/{1}'.format(success, total), success/total*100, '%\nerrors:', error, end =" ")
		if not error: print("no errors, great!")
		else: print()

if __name__=="__main__":
	if len(sys.argv) > 1:
		#py sdk.py easy all print
		main(sys.argv[1], sys.argv[2], None if len(sys.argv) == 3 else sys.argv[3])
	else: 
		#py sdk.py
		mode = input("mode ('macro' or 'single'): ")
		if mode == 'macro' or mode=='m':
			main(input("level(easy, medium, hard): "),  input("date(mmdd, all, latest): "), input("print? (n = Enter): "))
			quit()
			
		#input mode
		date = input("quizdate: ")
		level = input("quizlevel: ")
		grid = Board(_input=True)
		sdk = SudokuSolver(grid)
		save(level, date, sdk)

		sdk.solve()
		sdk.print()

		quit("see you next time")