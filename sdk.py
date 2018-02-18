#ToDo Next:
	#memoize the solved ones ->
		#or a save function for the answers

	#need better names for the methods

	#clean up code

from board import *
import csv, sys

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

	if date  == 'all':
		boards = read(level)[1:]
	else:
		if date == 'latest': 
			date = read(level)[-1][0]
		boards = list(filter(lambda x: x[0] == date, read(level)))
		
	if _print == '0': _print = False

	success, error = 0,0
	
	for board in boards:
		print(level, board[0])
		sdk = SudokuSolver(Board(board))
		sdk.solve()
		sdk.print(_print)

		if not sdk.solution.isLglSdk(): error +=1
		if sdk.solution.isLglSdk(1): success +=1
	total = len(boards)
	print('final grade: {0}/{1}'.format(success, total), success/total*100, '%\nerrors:', error, end =" -> ")
	if not error: 
		print("no errors, great!")
	else: print("fix yo errors")

if __name__=="__main__":
	if len(sys.argv) > 1:
		#py sdk.py easy all 
		#py sdk.py m latest 2
		main(sys.argv[1], sys.argv[2], None if len(sys.argv) == 3 else sys.argv[3])
	else: 
		#py sdk.py
		mode = input("mode ('macro' or 'single'): ")
		if mode == 'macro' or mode=='m':
			main(input("level(easy, medium, hard): "),  input("date(mmdd, all, latest): "), input("print? ('0','1','2'): "))
			quit()
			
		#input mode
		date = input("quizdate: ")
		level = input("quizlevel: ")
		grid = Board(_input=True)
		sdk = SudokuSolver(grid)
		save(level, date, sdk)

		main(level, date, input("print? "))

		quit("see you next time")