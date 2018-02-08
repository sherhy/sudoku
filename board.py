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

	#for making board via array inputs per rows
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
		# print(block)

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
		
		# if a:
		# 	print('A',end="->")
		# 	if b:
		# 		print('B',end="->")
		# 		if c: 
		# 			print('C',end=": ")
		
		if a and b and c: return True
		return False

	def isLglSdk(self):
		for row in self.grid:
			for i in row:
				if math.isnan(i): 
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
		
	def eliminate(self, a, ind):
		#eliminate candidate from row, col, block
		for i in range(9):
			self.maybe[ind[0]][i].discard(a)
		for i in range(9):
			self.maybe[i][ind[1]].discard(a)
		row = (ind[0]//3)*3
		col = (ind[1]//3)*3
		for i in range(3):
			for j in range(3):
				self.maybe[row + i][col + i].discard(a)

		self.maybe[ind[0]][ind[1]] = {a}
	
	def elimAll(self, board):
		#look at each provided answer and eliminate
		for i in range(9):
			for j in range(9):
				a = board.grid[i][j]
				if a != 0:
					self.eliminate(a, [i,j])

	def elimGrid(self, ind):
		#solve for unique in block
		row = ind[0]
		col = ind[1]
		block_candidate = []
		
		#collect candidate
		for i in range(3):
			for j in range(3):
				block_candidate += list(self.maybe[row+i][col+j])

		#change candidate set to which is unique in block
		for _ in range(1,10):
			if block_candidate.count(i) == 1:
				for i in range(3):
					for j in range(3):
						if self.maybe[row+i][col+j].intersection({_}):
							self.maybe[row+i][col+j] = {_}

	def elimGridAll(self):
		for i in range(3):
			for j in range(3):
				self.elimGrid([i*3,j*3])


class SudokuSolver():
	#this guy basically connects the candidate and solution
	def __init__(self, board):
		self.puzzle = board.grid #for reference
		self.candidate = Candidate(board) #to use when solving
		self.solution = self.candidate.deepcopy()

	def solve(self):
		counter = 0
		while True:
			#need a loop which stops when maybe grid doesn't change anymore
			counter +=1
			print(counter)
			mock = copy.deepcopy(self.candidate.maybe)
			self.candidate.elimAll(self.solution)
			self.candidate.elimGridAll()
			self.update()
			if mock == self.candidate.maybe: break



	def update(self):
		#find and update unique if only candidate left
		for i in range(9):
			for j in range(9):
				if len(self.candidate.maybe[i][j]) ==1: 
					self.solution.grid[i][j] = sum(list(self.candidate.maybe[i][j]))

		




