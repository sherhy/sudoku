#should write some concepts, dates, yada yada..

import copy, math, random

class Board():
	def __init__(self, arr = None, _input=False):
		self.grid = [ [0]*9 for row in range(9) ]
		self.answer = []
		self.maybe = []
		if arr != None:
			self.arr2grid(arr)

		if _input:
			self.inputGrid()

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
		for r in range(9):
			print('row', r+1,end=': ')
			query = [int(x) for x in input()]
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

	def arr2grid(self, board):
		#board = ['mmdd', 'numeric']
		for i in range(9):
			self.grid[i] = [int(x) for x in board[1][i*9:i*9+9]]

	def createBoard(self):
		#make question board (as hard as solving one)
		pass



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
		#returns a list of ints
		mayblock = []
		for i in range(3):
			for j in range(3):
				mayblock += list(self.maybe[ind[0]+i][ind[1]+j])
		return mayblock

	def RC(self, ind): 
		#solve for unique candidate in row and col
		row, col = ind[0], ind[1]
		
		#collect for row and col
		maycol = [self.maybe[x][col] for x in range(9)] 
		mayrow = [self.maybe[row][y] for y in range(9)]

		for digit in range(1,10):
			#i want to have returned indices for where digits exist
			colind = [y for y in range(9) if len(mayrow[y].intersection({digit})) == 1 ]
			rowind = [x for x in range(9) if len(maycol[x].intersection({digit})) == 1 ]

			if len(colind) == 1: 
				self.maybe[row][colind[0]] = {digit}

			if len(rowind) == 1: 
				self.maybe[rowind[0]][col] = {digit}

	def Block(self, ind):
		#solve for unique candidate in block
		row, col = ind[0], ind[1]
		
		#collect block.candidate
		mayblock = self.maybeBlock([row,col])

		#change candidate set to which is unique in block
		for digit in range(1,10):
			if mayblock.count(digit) == 1:
				for i in range(3):
					for j in range(3):
						if self.maybe[row+i][col+j].intersection({digit}):
							self.maybe[row+i][col+j] = {digit}

	def Linear(self, ind):
		#delete candidate in other blocks if pair colinear
		#feels like this should go to Candidate class
		row, col = ind[0],ind[1]

		#collect block.candidate
		mayblock = self.maybeBlock([row,col])

		for digit in range(1,10):
			if mayblock.count(digit) == 2:
				#find the two coords
				match1, match2 = [],[]
				for i in range(3):
					for j in range(3):
						if self.maybe[row+i][col+j].intersection({digit}):
							if match1 == []: match1 = [row+i,col+j]
							else:
								match2 = [row+i,col+j]
				if match1[0] == match2[0]:
					#same row
					for j in range(9):
						if j != match1[1] and j != match2[1]:
							self.maybe[match1[0]][j].discard(digit)
				if match1[1] == match2[1]:
					#same col
					for i in range(9):
						if i != match1[0] and i != match2[0]:
							self.maybe[i][match1[1]].discard(digit)

							
	def PairsBlk(self, ind):
		#erase candidate from block that has space-exhaustive pairs
		row , col = ind[0], ind[1]

		#array of list(row) 
		layerblock = [self.maybe[row+i][col:col+3] for i in range(3)]
		
		#array of set 
		mayblock = [item for layer in layerblock for item in layer]

		#find hidden pairs
		#make data for indices 
		digit_dict = dict()
		for digit in range(1,10):
			inds = [i for i in range(9) if digit in mayblock[i]]
			count = len(inds)
			digit_dict[digit] = inds

		#find match
		for i in range(1,10):
			#numbers NOT indices of block
			match =[j for j in range(i,10) if digit_dict[i]==digit_dict[j]] 
			if len(match) == len(digit_dict[i]):
				#readjust for block
				for x in range(9):
					if mayblock[x].intersection(set(match)) == set(match):
						mayblock[x] = set(match)

		# #WRONG (but keeping it)
		# for i in mayblock:
		# 	diff = [i.difference(j) for j in mayblock if len(i.difference(j))>1]
		# 	# print('diff',diff)
		# 	if len(diff) < 1: continue
		# 	comm = diff[0]
		# 	for j in diff:
		# 		comm = comm.intersection(j)
		# 	if len(comm)>1 and len(list(filter(lambda x: x.intersection(comm), mayblock)))==len(comm):
		# 		mayblock = [comm if comm.intersection(b) == comm else b for b in mayblock]

		#array of set longer than two
		short = list(filter(lambda x: len(x)>1, mayblock))
		
		#short might already have a matching pair, 
		#(eg. pair of {4,8} must delete 4 and 8 from other candidates)
		for i in short:
			match = list(filter(lambda x: i == x, short))
			if len(match) == len(i): 
				#this conditional means that ie pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(mayblock)):
					for x in nums:	
						if mayblock[s] != i: 
							# print('deleting {} from {}'.format(x, mayblock[s]))
							mayblock[s].discard(x)

		#recalibrate the candidate grid
		for i in range(3):
			for j in range(3):
				self.maybe[row+i][col+j] = mayblock.pop(0)

	def PairsRC(self, ind):
		#erase candidate from row col that have space-exhaustive pairs
		row , col = ind[0], ind[1]

		#array of sets
		maycol = [self.maybe[x][col] for x in range(9)] 
		mayrow = [self.maybe[row][x] for x in range(9)]

		# #find hidden pairs
		digit_dict = dict()
		for digit in range(1,10):
			inds = [i for i in range(9) if digit in maycol[i]]
			count = len(inds)
			digit_dict[digit] = inds

		#find match
		for i in range(1,10):
			#numbers NOT indices of block
			match =[j for j in range(i,10) if digit_dict[i]==digit_dict[j]] 
			if len(match) == len(digit_dict[i]):
				#readjust for block
				for x in range(9):
					if maycol[x].intersection(set(match)) == set(match):
						maycol[x] = set(match)

		digit_dict = dict()
		for digit in range(1,10):
			inds = [i for i in range(9) if digit in mayrow[i]]
			count = len(inds)
			digit_dict[digit] = inds

		#find match
		for i in range(1,10):
			#numbers NOT indices of block
			match =[j for j in range(i,10) if digit_dict[i]==digit_dict[j]] 
			if len(match) == len(digit_dict[i]):
				#readjust for block
				for x in range(9):
					if mayrow[x].intersection(set(match)) == set(match):
						mayrow[x] = set(match)

		# #WRONG (but keeping it)
		# for i in maycol:
		# 	diff = [i.difference(j) for j in maycol if len(i.difference(j))>1]
		# 	# print('diff',diff)
		# 	if len(diff) < 1: continue
		# 	comm = diff[0]
		# 	for j in diff:
		# 		comm = comm.intersection(j)
		# 	if len(comm)>1 and len(list(filter(lambda x: x.intersection(comm), maycol)))==len(comm):
		# 		maycol = [comm if comm.intersection(b) == comm else b for b in maycol]
		# for i in mayrow:
		# 	diff = [i.difference(j) for j in mayrow if len(i.difference(j))>1]
		# 	# print('diff',diff)
		# 	if len(diff) < 1: continue
		# 	comm = diff[0]
		# 	for j in diff:
		# 		comm = comm.intersection(j)
		# 	if len(comm)>1 and len(list(filter(lambda x: x.intersection(comm), mayrow)))==len(comm):
		# 		mayrow = [comm if comm.intersection(b) == comm else b for b in mayrow]

		#array of sets with mutliple candidate
		shortrow = list(filter(lambda x: len(x)>1, mayrow))
		shortcol = list(filter(lambda x: len(x)>1, maycol))

		for i in shortrow:
			match = list(filter(lambda x: i == x, shortrow))
			if len(match) == len(i): 
				#this conditional means that eg pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(mayrow)):
					for x in nums:	
						if mayrow[s] != i: 
							mayrow[s].discard(x)
		for i in range(9):
			self.maybe[row][i] = mayrow.pop(0)

		for i in shortcol:
			match = list(filter(lambda x: i == x, shortcol))
			if len(match) == len(i): 
				#this conditional means that pairs of 3 candidate must have 3 matching pairs
				nums = list(i)
				for s in range(len(maycol)):
					for x in nums:	
						if maycol[s] != i: 
							maycol[s].discard(x)

		for i in range(9):
			self.maybe[i][col] = maycol.pop(0)

	def RCBlock(self, ind):
		#reduces candidates to a certain row/col of the block 
		#by looking at candidates in the row/col outside the block
		row , col = ind[0], ind[1]

		maycols = [[self.maybe[x][col+i] for x in range(9)] for i in range(3)]
		
		for x in range(3):
			#x refers to col
			#save indices containing digit
			for digit in range(1,10):
				indrows = set(y for y in range(9) if digit in maycols[x][y])
				if len(indrows)<2 or len(set(i for i in range(row,row+3)).union(indrows)) > 3: 
					continue

				for p in range(3):
					for q in range(3):
						if q == x: continue
						if digit in self.maybe[row+p][col+q]:
							self.maybe[row+p][col+q].discard(digit)
							# print('d {} from {}'.format(digit, [row+p, col+q]))

	def xWing(self):
		pass



class SudokuSolver():
	#this guy basically connects the candidate and solution
	def __init__(self, board):
		self.puzzle = board.grid #for reference
		self.candidate = Candidate(board) #to use when solving
		self.solution = self.candidate.deepcopy()

	def checkMemo(self):
		pass

	def solve(self):
		if self.checkMemo(): 
			pass
		counter = 0
		while True:
			mock = copy.deepcopy(self.candidate.maybe)
			self.oneLoop()
			if mock == self.candidate.maybe: break

	def print(self, _opt = False):
		#_opt 0: no print / 1: print solution / 2: print candidate
		if bool(_opt) != True: return None
		if _opt =='1': self.solution.print()
		if _opt =='2': self.candidate.print(2)
		print('sudoku_complete()', self.solution.isLglSdk(1))

	def oneLoop(self):
		self.candidate.elimAll(self.solution)
		self.logicBlkAll()
		self.logicRCAll()
		self.candidate.xWing()
		self.updateGrid()

	def logicBlkAll(self):
		for i in range(0,9,3):
			for j in range(0,9,3):
				self.candidate.Block([i,j])
				self.candidate.Linear([i,j])
				self.candidate.PairsBlk([i,j])
				self.candidate.RCBlock([i,j])

	def logicRCAll(self):
		for i in range(9):
			for j in range(9):			
				self.candidate.PairsRC([i,j])
			self.candidate.RC([i,j])				
				
	def updateGrid(self):
		#convert singled out candidate to solution grid
		for i in range(9):
			for j in range(9):
				if len(self.candidate.maybe[i][j]) ==1:
					digit = sum(list(self.candidate.maybe[i][j]))	
					self.solution.grid[i][j] = digit