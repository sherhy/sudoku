#find hidden pair
block=[
{3,4,5,9},{1,3,8,9},{1,3,5,7,8},
{3,4,5,9},			{6},				{2},
{3,4,5,9},		{3,9},		{3,5,7}]

newblock=[
{9, 3, 4, 5}, {8, 1}, {8, 1}, 
{9, 3, 4, 5}, {6}, {2}, 
{9, 3, 4, 5}, {9, 3}, {3, 5, 7}]

#nvermind triples, first find pairs:
print(block)

#make data for indices 
digit_dict = dict()
for digit in range(1,10):
	inds = [i for i in range(9) if digit in block[i]]
	count = len(inds)
	digit_dict[digit] = inds

# for x in digit_dict:
# 	print(x, digit_dict[x])

#find match
for i in range(1,10):
	#numbers NOT indices of block
	match =[j for j in range(i,10) if digit_dict[i]==digit_dict[j]] 
	if len(match) == len(digit_dict[i]):
		#readjust for block
		for x in range(9):
			if block[x].intersection(set(match)) == set(match):
				block[x] = set(match)

print(block)




# print( list(filter(lambda x: len(x) >1, block)) )

# comms = []
# for i in block:
# 	diff = [i.difference(j) for j in block if len(i.difference(j))>1]
# 	# print('diff',diff)
# 	if len(diff) < 1: continue
# 	comm = diff[0]
# 	for j in diff:
# 		comm = comm.intersection(j)
# 	if len(comm)>1 and len(list(filter(lambda x: x.intersection(comm), block)))==len(comm):
# 		print(i,'comm',comm)
# 		block = [comm if comm.intersection(b) == comm else b for b in block]
# 		# comms.append(comm)