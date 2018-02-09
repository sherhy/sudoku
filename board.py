import copy, math, random

class Board():
	def __init__(self):
		self.grid = [ [0]*9 for row in range(9) ]
		self.answer = []
		self.maybe = []

	def print(self, opt = 0):
		option = [self.grid, self.answer, self.maybe]
		if option[opt] == False: print('False')
		maxChar = 0
		for row in option[opt]:
			for i in row:
				maxChar = max([len(str(i)) , maxChar])
		formatSpecInt = '%'+str(maxChar)+'d'
		formatSpecStr = '%'+str(maxChar)+'s'
		width = ' '
		rCount = 0
		cCount = 0
		for row in option[opt]:
			for i in row:
				if isinstance(i, int):
					print(formatSpecInt%i, end=width)
				else: print(formatSpecStr%i, end=width)
				
				cCount +=1
				if cCount %3==0:
					print(end=width)
			rCount +=1
			if rCount%3==0: 
				print('\n')
			else:
				print()

	#for making board via array inputs per row
	def inputGrid(self):
		for r in range(len(self.grid)):
			print('row')
			query = [int(x) for x in input().split(',')]
			row = []
			for i in query:
				if i == 0: row.append(float('nan'))
				else: row.append(i)
			self.grid[r] = row

	def deepcopy(self):
		c = Board()
		c.grid = copy.deepcopy(self.grid)
		return c

	def isLglRow(self, row):
		duplicates =[]
		for i in self.grid[row]:
			if i == 0 or i == float('nan'): continue
			if i in duplicates: return False
			duplicates.append(i)
		return True

	def isLglCol(self, col):
		duplicates = []
		for i in range(len(self.grid)):
			if self.grid[i][col] == 0 or self.grid[i][col] == float('nan'): continue
			if self.grid[i][col] in duplicates: return False
			duplicates.append(self.grid[i][col])
		return True

	def isLglBlk(self, index):
		#index takes in [0-2,0-2]
		row, col = index[0]*3,index[1]*3
		block = []
		for i in range(row, row+3):
			block.append(self.grid[i][col:col+3])

		duplicates =[]
		for row in block:
			for i in row:
				if i == 0 or i == float('nan'): continue
				if i in duplicates: return False
				duplicates.append(i)
		return True	

	def isLglVal(self, a, index):
		psb = self.deepcopy()
		psb.grid[index[0]][index[1]] = a
		a = psb.isLglRow(index[0])
		b = psb.isLglCol(index[1])
		c = psb.isLglBlk([index[0]//3, index[1]//3])

		if a and b and c: return True
		return False

	def isLglSdk(self, option = 0):
		if option:
			for row in self.grid:
				for i in row:
					if math.isnan(i) or i==0: 
						return False

		for i in range(9):
			if not self.isLglRow( i): return False
		for i in range(9):
			if not self.isLglCol(i): return False
		for i in range(3):
			for j in range(3):
				if not self.isLglBlk( [i,j]): return False
		return True
	








class TrainingBoard(Board):
	def __init__(self, arr = None):
		super(TrainingBoard, self).__init__()
		self.answer=[ [0]*9 for row in range(9) ]
		if arr != None:
			self.arr2grid(arr)
		else:
			self.createBoard()
	
	def arr2grid(self, arr):
		for i in range(9):
			self.grid[i] = [int(x) for x in arr[0][i*9:i*9+9]]
			if len(arr)==2:
				self.answer[i] = [int(x) for x in arr[1][i*9:i*9+9]]

	def createBoard(self):
		#make question board (as hard as solving one)
		pass










class Candidate(Board):
	def __init__(self, board=None):
		super(Candidate, self).__init__()
		#1-9 for each index
		self.maybe = [[{x for x in range(1,10)} for i in range(9)] for i in range(9)]

		if board != None:
			self.grid = board.grid
		
	def elimRowCol(self, a, ind, replace=True):
		#eliminate candidate from row & col
		for i in range(9):
			self.maybe[ind[0]][i].discard(a)
			self.maybe[i][ind[1]].discard(a)
		if replace:
			self.maybe[ind[0]][ind[1]] = {a}

	def elimBlk(self, a, ind, replace=True):
		#eliminate candidate from block
		row, col = (ind[0]//3)*3, (ind[1]//3)*3
		for i in range(3):
			for j in range(3):
				self.maybe[row + i][col + j].discard(a)

		if replace: 
			self.maybe[ind[0]][ind[1]] = {a}
	
	def elimAll(self, board):
		#look at solution and eliminate candidate
		for i in range(9):
			for j in range(9):
				a = board.grid[i][j]
				if a != 0:
					self.elimBlk(a, [i,j])
					self.elimRowCol(a, [i,j])
	








class SudokuSolver():
	#this guy basically connects the candidate and solution
	def __init__(self, board):
		self.puzzle = board.grid #for reference
		self.candidate = Candidate(board) #to use when solving
		self.solution = self.candidate.deepcopy()

	def oneLoop(self):
		self.candidate.elimAll(self.solution)

		self.logicBlkAll()
		self.logicRowColAll()
		self.updateGrid()

	def solve(self):
		counter = 0
		while True:
			#need a loop which stops when maybe grid doesn't change anymore
			counter +=1
			if counter > 10000: 
				print(counter)

			mock = copy.deepcopy(self.candidate.maybe)
			self.oneLoop()
			if mock == self.candidate.maybe: break

	def print(self):
		self.solution.print()
		self.candidate.print(2)
		print('sudoku_complete()', self.solution.isLglSdk(1))

	def logicBlk(self, ind):
		#solve for unique candidate in block
		row, col = ind[0], ind[1]
		block_maybe = []
		
		#collect block.candidate
		for i in range(3):
			for j in range(3):
				block_maybe += list(self.candidate.maybe[row+i][col+j])

		#change candidate set to which is unique in block
		for digit in range(1,10):
			if block_maybe.count(digit) == 1:
				for i in range(3):
					for j in range(3):
						if self.candidate.maybe[row+i][col+j].intersection({digit}):
							self.candidate.maybe[row+i][col+j] = {digit}
							self.solution.grid[row+i][col+j] = digit					
								
	def logicBlkAll(self):
		for i in range(0,9,3):
			for j in range(0,9,3):
				self.logicBlk([i,j])
				self.logicLinear([i,j])

	def logicRowCol(self, ind): #-> turns out to be redundant;;
		#solve for unique candidate in rowcol
		row, col = ind[0], ind[1]
		
		#collect for array
		row_maybe = [self.candidate.maybe[x][col] for x in range(9) if x!= row] 
		col_maybe = [self.candidate.maybe[row][x] for x in range(9) if x!= col]

		for digit in range(1,10):
			#check if he's the only guy in the row or col
			rowCheck = list(filter(lambda i: i.intersection({digit}), row_maybe))
			colCheck = list(filter(lambda i: i.intersection({digit}), col_maybe))
		
		# print([i,j], digit, rowCheck, colCheck)
		if rowCheck == [] or colCheck==[]: 
			self.candidate.maybe[row][col] = {digit}
			self.solution.grid[row][col] = digit

	def logicLinear(self, ind):
		#delete candidate in other blocks if pair colinear
		#feels like this should go to Candidate class
		row, col = ind[0],ind[1]
		block_maybe = []
		#collect block.candidate
		for i in range(3):
			for j in range(3):
				block_maybe += list(self.candidate.maybe[row+i][col+j])

		for digit in range(1,10):
			if block_maybe.count(digit) == 2:
				#find the two coords
				match1, match2 = [],[]
				for i in range(3):
					for j in range(3):
						if self.candidate.maybe[row+i][col+j].intersection({digit}):
							if match1 == []: match1 = [row+i,col+j]
							else:
								match2 = [row+i,col+j]
				if match1[0] == match2[0]:
					#same row
					for j in range(9):
						if j != match1[1] and j != match2[1]:
							self.candidate.maybe[match1[0]][j].discard(digit)
				if match1[1] == match2[1]:
					#same col
					for i in range(9):
						if i != match1[0] and i != match2[0]:
							self.candidate.maybe[i][match1[1]].discard(digit)

	
	def logicRowColAll(self):
		for i in range(9):
			for j in range(9):
				self.logicRowCol([i,j])


	def updateGrid(self):
		for i in range(9):
			for j in range(9):
				if len(self.candidate.maybe[i][j]) ==1:
					digit = sum(list(self.candidate.maybe[i][j]))	
					self.solution.grid[i][j] = digit


		




