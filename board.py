#should write some concepts, dates, yada yada..

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
		rCount, cCount = 0, 0
		for row in option[opt]:
			for i in row:
				if isinstance(i, int): print(formatSpecInt%i, end=width)
				else: print(formatSpecStr%i, end=width)
				
				cCount +=1
				if cCount %3==0: print(end=width)
			rCount +=1
			if rCount%3==0: print('\n')
			else: print()
	
	def inputGrid(self):
		#for making board via array inputs per row
		for r in range(len(self.grid)):
			print('row')
			query = [int(x) for x in input().split(',')]
			row = [0 if (i ==0 or i == float('nan')) else i for i in query]
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
		#is legal sudoku, option = 1 being strict
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
#
#
#
#
#
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
			self.answer[i] = [int(x) for x in arr[1][i*9:i*9+9]] if len(arr)==2 else []

	def createBoard(self):
		#make question board (as hard as solving one)
		pass
#
#
#
#
#
class Candidate(Board):
	def __init__(self, board=None):
		super(Candidate, self).__init__()
		#1-9 for each index
		self.maybe = [[{x for x in range(1,10)} for i in range(9)] for i in range(9)]

		if board != None: self.grid = board.grid

	def elimAll(self, board):
		#look at solution and eliminate candidate
		for i in range(9):
			for j in range(9):
				a = board.grid[i][j]
				if a != 0:
					self.elimBlk(a, [i,j])
					self.elimRowCol(a, [i,j])

	def elimBlk(self, a, ind, replace=True):
		#eliminate candidate from block
		row, col = (ind[0]//3)*3, (ind[1]//3)*3
		for i in range(3):
			for j in range(3):
				self.maybe[row + i][col + j].discard(a)

		if replace: 
			self.maybe[ind[0]][ind[1]] = {a}		

	def elimRowCol(self, a, ind, replace=True):
		#eliminate candidate from row & col
		for i in range(9):
			self.maybe[ind[0]][i].discard(a)
			self.maybe[i][ind[1]].discard(a)
		if replace:
			self.maybe[ind[0]][ind[1]] = {a}

	def maybeBlock(self, ind, option=False):
		mayblock = []
		for i in range(3):
			for j in range(3):
				if option:
					mayblock += self.maybe[ind[0]+i][ind[1]+j]
				else:
					mayblock += list(self.maybe[ind[0]+i][ind[1]+j])
		return mayblock

#
#	
#
#
#
#
#
#
#
#
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
			if counter > 1000: 
				print(counter)

			mock = copy.deepcopy(self.candidate.maybe)
			self.oneLoop()
			if mock == self.candidate.maybe: break

	def print(self):
		self.solution.print()
		self.candidate.print(2)
		print('sudoku_complete()', self.solution.isLglSdk(1))

	def oneLoop(self):
		self.candidate.elimAll(self.solution)

		self.logicBlkAll()
		self.logicRowColAll()
		self.updateGrid()

	def logicBlkAll(self):
		for i in range(0,9,3):
			for j in range(0,9,3):
				self.logicBlk([i,j])
				self.logicLinear([i,j])
				self.logicPairsBlk([i,j])

	def logicBlk(self, ind):
		#solve for unique candidate in block
		row, col = ind[0], ind[1]
		
		#collect block.candidate
		mayblock = self.candidate.maybeBlock([row,col])

		#change candidate set to which is unique in block
		for digit in range(1,10):
			if mayblock.count(digit) == 1:
				for i in range(3):
					for j in range(3):
						if self.candidate.maybe[row+i][col+j].intersection({digit}):
							self.candidate.maybe[row+i][col+j] = {digit}
							self.solution.grid[row+i][col+j] = digit					

	def logicLinear(self, ind):
		#delete candidate in other blocks if pair colinear
		#feels like this should go to Candidate class
		row, col = ind[0],ind[1]
		#collect block.candidate
		mayblock = self.candidate.maybeBlock([row,col])

		for digit in range(1,10):
			if mayblock.count(digit) == 2:
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
								
	def logicPairsBlk(self, ind):
		#this, too.. should belong in the candidate class
		#erase candidate from block that has space-exhaustive pairs
		row , col = ind[0], ind[1]

		#array of list(row) 
		layerblock = [self.candidate.maybe[row+i][col:col+3] for i in range(3)]
		#array of set 
		mayblock = [item for layer in layerblock for item in layer]

		#array of set longer than two
		bshort = list(filter(lambda x: len(x)>1, mayblock))
		
		#bshort might already have a matching pair, 
		#(eg. pair of {4,8} must delete 4 and 8 from other candidates)
		for i in bshort:
			match = list(filter(lambda x: i == x, bshort))
			if len(match) == len(i): 
				#this conditional means that ie pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(mayblock)):
					for x in nums:	
						if mayblock[s] != i: 
							# print('deleting {} from {}'.format(x, mayblock[s]))
							mayblock[s].discard(x)

		#recalibrate the maybe grid
		for i in range(3):
			for j in range(3):
				self.candidate.maybe[row+i][col+j] = mayblock.pop(0)

	def logicRowColAll(self):
		for i in range(9):
			for j in range(9):
				self.logicRowCol([i,j])
				self.logicPairsRC([i,j])

	def logicRowCol(self, ind): #-> turns out to be redundant;;
		#solve for unique candidate in rowcol
		row, col = ind[0], ind[1]
		
		#collect for array
		col_maybe = [self.candidate.maybe[x][col] for x in range(9) if x!= row] 
		row_maybe = [self.candidate.maybe[row][x] for x in range(9) if x!= col]

		for digit in range(1,10):
			#check if he's the only guy in the row or col
			rowCheck = list(filter(lambda i: i.intersection({digit}), row_maybe))
			colCheck = list(filter(lambda i: i.intersection({digit}), col_maybe))
		
		# print([i,j], digit, rowCheck, colCheck)
		if rowCheck == [] or colCheck==[]: 
			self.candidate.maybe[row][col] = {digit}
			self.solution.grid[row][col] = digit

	def logicPairsRC(self, ind):
		#applying same logic for logicPairsBlk
		row , col = ind[0], ind[1]

		#array of sets
		maycol = [self.candidate.maybe[x][col] for x in range(9)]# if x!= row] 
		mayrow = [self.candidate.maybe[row][x] for x in range(9)]# if x!= col]

		# #array of int
		# mayrow = [item for layer in row_maybe for item in layer]
		# maycol = [item for layer in col_maybe for item in layer]

		#array of sets with mutliple candidate
		bshortrow = list(filter(lambda x: len(x)>1, mayrow))
		bshortcol = list(filter(lambda x: len(x)>1, maycol))

		for i in bshortrow:
			match = list(filter(lambda x: i == x, bshortrow))
			if len(match) == len(i): 
				#this conditional means that eg pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(mayrow)):
					for x in nums:	
						if mayrow[s] != i: 
							mayrow[s].discard(x)
		for i in range(9):
			self.candidate.maybe[row][i] = mayrow.pop(0)

		for i in bshortcol:
			match = list(filter(lambda x: i == x, bshortcol))
			if len(match) == len(i): 
				#this conditional means that pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(maycol)):
					for x in nums:	
						if maycol[s] != i: 
							maycol[s].discard(x)

		for i in range(9):
			self.candidate.maybe[i][col] = maycol.pop(0)


	
	def updateGrid(self):
		#convert singled out candidate to solution grid
		for i in range(9):
			for j in range(9):
				if len(self.candidate.maybe[i][j]) ==1:
					digit = sum(list(self.candidate.maybe[i][j]))	
					self.solution.grid[i][j] = digit


