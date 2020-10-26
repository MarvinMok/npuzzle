import collections
import heapq


#globals for efficiency
goal = None
n = None
statelen = None

# Loads file to create board
# Arguemnts: file
# Returns: tuple
def loadFromFile(file):
	global goal
	global n
	global statelen

	#opens file and converts into 1D representation of board
	with open (file, 'r') as f:

		#n isnumber of rows or columns
		n = int(f.readline()[0])
		#print (n)
		board = []
		for i in range(0, n):
			l = f.readline().strip().split()
			board = board + l
		board = [0 if e == '*' else int(e) for e in board]

		#solution board
		goal = tuple(list(range(1, len(board))) + [0])

		#length of board in 1D or n ** 2
		statelen = n**2

		#print (board)
		return tuple(board)

# Computes Neighbors
# Arguemnts: tuple, int
# Returns: tuple with tuples of (int, tuple)
def computeNeighbors(state, last = -1):

	global statelen
	global n
	# rows is //, columns is %
	#location of 0 (aka where to swap with)
	i = state.index(0)

	#print(i)
	#print (neighborslocations)
	neighbors = [] 

	#t is location of neighbor

	#neighbor to the left
	t = i - 1
	if t != last and t // n == i // n:
		temp = list(state)
		neighbor = state[t]
		temp[i] = neighbor
		temp[t] = 0
		
		neighbors.append((neighbor, tuple(temp)))
		#neighbors.append(neighbor)


	#neighbor below
	t = i - n
	if t != last and t >= 0:
		temp = list(state)
		neighbor = state[t]
		temp[i] = neighbor
		temp[t] = 0
		
		neighbors.append((neighbor, tuple(temp)))
		#neighbors.append(neighbor)

	#neighbor above
	t = i + 1
	if t != last and t // n == i // n:
		temp = list(state)
		neighbor = state[t]
		temp[i] = neighbor
		temp[t] = 0
		
		neighbors.append((neighbor, tuple(temp)))

	#neighbor to the right
	t = i + n
	if t != last and t < statelen:
		temp = list(state)
		neighbor = state[t]
		temp[i] = neighbor
		temp[t] = 0
		
		neighbors.append((neighbor, tuple(temp)))



	return neighbors #zip(neighbors, newstates)

# checks if state is Goal
# Arguemnts: tuple
# Returns: boolean
def isGoal(state):

	global goal
	global statelen

	#checks if values of goal are the same as state
	for i in range(0, statelen):
		if goal[i] != state[i]:
			return False

	return True

# Prints state in readable form
# Arguemnts: state
# Returns: None
def debugPrint(state):
	n =round((len(state) + 1) ** 0.5) 
	for i in range(0, n):
		print(state[i * n: (i + 1) * n])

# Breadth First Search
# Arguemnts: tuple
# Returns: list
def BFS(state):

	#deque for efficency
	frontier = collections.deque([state])

	#set of discovered states
	discovered = {tuple(state)}

	#moves to get to a given state
	parents = {tuple(state): None}
	expanded = 0

	#solves puzzle
	while frontier:

		#gets current state
		currentstate = frontier.popleft()
		expanded += 1
		#if expanded % 100 == 0:
			#print (expanded)
		#discovered.add(tuple(currentstate)) 

		#checks if solution
		if isGoal(currentstate):
			return parents[tuple(currentstate)]

		#computes neighbors and adds them to parents, frontier, and discovered if not discovered	
		for neighbor in computeNeighbors(currentstate):
			if tuple(neighbor[1]) not in discovered:
				frontier.append(neighbor[1])
				discovered.add(tuple(neighbor[1]))
				if(not parents[tuple(currentstate)]):
					parents[tuple(neighbor[1])] = [neighbor[0]]
				else:
					parents[tuple(neighbor[1])] = parents[tuple(currentstate)] + [neighbor[0]]


# Depth First Search
# Arguemnts: tuple
# Returns: list
def DFS(state):

	frontier = [state]

	#set of discovered states
	discovered = {tuple(state)}

	#moves to get to a given state
	parents = {tuple(state): None}
	expanded = 1

	#solves puzzle
	while frontier:
		expanded += 1
		if expanded % 100 == 0:
			print (expanded)

		#gets current state
		currentstate = frontier.pop()
		discovered.add(tuple(currentstate)) 
		
		#checks if solution
		if isGoal(currentstate):
			return parents[tuple(currentstate)]

		#computes neighbors and adds them to parents, frontier, and discovered if not discovered
		for neighbor in computeNeighbors(currentstate):
			if tuple(neighbor[1]) not in discovered:
				frontier.append(neighbor[1])
				discovered.add(tuple(neighbor[1]))
				if(not parents[tuple(currentstate)]):
					parents[tuple(neighbor[1])] = [neighbor[0]]
				else:
					parents[tuple(neighbor[1])] = parents[tuple(currentstate)] + [neighbor[0]]


#BiDirectional Search
# Arguemnts: tuple
# Returns: list				
def Bidirectionalsearch(state):
	global n 
	global goal


	#print("in b")
	#print(goal)

	#set up for BFS from the original state
	frontierFromSource = collections.deque([state])
	discoveredFromSource = {state}
	parentsFromSource = {state: []}
	

	#set up for BFS from the goal
	frontierFromGoal = collections.deque([goal])
	#print (frontierFromGoal)
	discoveredFromGoal = {goal}
	parentsFromGoal = {goal: []}


	lastMoveSource = -1
	lastMoveGoal = -1
	#x = 0
		#print(x)
	
	#solves puzzle
	while frontierFromGoal or frontierFromSource:
		#print(x)


		
		#gets current state
		currentstateSource = frontierFromSource.popleft()
		currentstateGoal = frontierFromGoal.popleft()
		
		discoveredFromSource.add(currentstateSource) 
		discoveredFromGoal.add(currentstateGoal) 


		

		#print (discoveredFromGoal & discoveredFromSource)
		#checks if solution
		if discoveredFromGoal & discoveredFromSource:
			temp = (discoveredFromGoal & discoveredFromSource).pop()
			#print (temp)
			#print (parentsFromSource)
			#print (parentsFromGoal)

			return parentsFromSource[temp] + parentsFromGoal[temp][::-1]

		#computes neighbors and adds them to parents, frontier, and discovered if not discovered
		for neighbor in computeNeighbors(currentstateSource, lastMoveSource):
			#print("infor0")
			newstate = neighbor[1]
			if newstate not in discoveredFromSource:
				frontierFromSource.append(newstate)
				discoveredFromSource.add(newstate)
				parentsFromSource[newstate] = parentsFromSource[currentstateSource] + [neighbor[0]]


		#print(computeNeigborhors(currentstateGoal))

		#computes neighbors and adds them to parents, frontier, and discovered if not discovered
		for neighbor in computeNeighbors(currentstateGoal, lastMoveGoal):
			newstate = neighbor[1]
			#print(neighbor[1])
			if newstate not in discoveredFromGoal:
				frontierFromGoal.append(newstate)
				discoveredFromGoal.add(newstate)
				parentsFromGoal[newstate] = parentsFromGoal[currentstateGoal] + [neighbor[0]]


		lastMoveSource = currentstateSource.index(0)
		lastMoveGoal = currentstateSource.index(0)
		#print (frontierFromGoal)


#Manhattan Heuristic
# Arguemnts: tuple
# Returns: int
def accH(currentstate):
	global n
	global statelen
	global goal

	a = 0

	#goes through each value of currentstate and sums manhattan distance
	for i in range(0, statelen):

		c = currentstate[i]
		if c != 0:

			g = c - 1
			#print ("g: " + str(g))
			m = abs(i % n - g % n) + abs(i // n - g // n)
			#print(str(c) + ": " + str(m))
			a += m



	return a


#Manhattan Heuristic
# Arguemnts: tuple, int
# Returns: int
def accH2(neighbor, laststateacc):
	global n
	global statelen
	global goal
	currentstate = neighbor[1]
	move = neighbor[0]


	
	# gets index of last move and new move
	index0 = currentstate.index(0)
	indexm = currentstate.index(move)
	g = move - 1

	#calculates manhattan distance
	m0 = abs(index0 % n - g % n) + abs(index0 // n - g // n)
	mm = abs(indexm % n - g % n) + abs(indexm // n - g // n)

	#returns h(x), since only two squares are changing form the last state
	return laststateacc + mm - m0

# AStar Search
# Arguemnts: tuple
# Returns: int
def AStar(state):

	global goal

	#setup similar to BFS, but frontier now contains tupes with (weight, state)
	laststateacc = accH(state)
	frontier = [(laststateacc, state)]

	discovered = {state}
	parents = {state: []}

	lastMove = -1

	#solves puzzles
	while frontier:
		#print (x)
		#heapq to efficiently create priority Queue
		temp = heapq.heappop(frontier)
		currentstate = temp[1]
		laststateacc = temp[0] - len(parents[currentstate])
		#print(currentstate)


		#discovered.add(tuple(currentstate)) 
		#checks if solution
		if isGoal(currentstate):
			#print (parents)
			print(nodes)
			return parents[currentstate]

		#computes neighbors and adds them to parents, frontier, and discovered if not discovered
		for neighbor in computeNeighbors(currentstate, lastMove):
			newstate = neighbor[1]
			if newstate not in discovered:

				discovered.add(newstate)
				parents[newstate] = parents[currentstate] + [neighbor[0]]

				temp = (accH2(neighbor, laststateacc) + len(parents[newstate]), newstate)
				heapq.heappush(frontier, temp)

		lastMove = currentstate.index(0)
		#print (frontierFromGoal)



# Checks if solution is valid
# Arguemnts: tuple, list
# Returns: boolean

def check(start, answer):
	temp = list(start)
	for e in answer:
		indexofzero = temp.index(0)
		indexofval = temp.index(e)
		temp[indexofzero] = e
		temp[indexofval] = 0
	return isGoal(temp)


# tesing ground
def main():

	board = loadFromFile('puzzle.txt')
	#print(goal)
	#print(n)
	#print(list(computeNeigborhors(board)))
	#print(isGoal(board))
	#debugPrint(board)
	#debugPrint(goal)
	#print(BFS(board))
	#print(DFS(board))

	#print(Bidirectionalsearch(board))

	star = AStar(board)
	print(star)
	print(check(board, star))


	#print(accH(board))







if __name__ == '__main__':
	main()