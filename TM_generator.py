import itertools as it
import pickle
import gzip
from tqdm import tqdm


def TM_max_state_use(machine, k):
	states = [chr(ord("A") + i) for i in range(k)]
	parts = machine.split("_")
	#get possible states an arbitrary state can transition to
	connec = {state: set() for state in states}

	for i, state in enumerate(states):
		part = parts[i]
		#get states given symbol reading of 0 and 1 respectively
		#ex: 1LA1RB -> s0 = A; s1 = B; here A0 maps to transition 1LA
		# and A1 maps to transition 1RB
		s0, s1 = part[2], part[5] 
		# add states to connec
		if s0 in states:
			connec[state].add(s0)
		if s1 in states:
			connec[state].add(s1)

	# DFS (e.g. https://en.wikipedia.org/wiki/Depth-first_search) from state A
	visited = set()
	stack = ["A"]
	while stack:
		curr = stack.pop() #take last state of the stack
		if curr in visited: #if state already visited
			continue
		visited.add(curr)
		stack.extend(connec[curr] - visited) #get unvisited states
	return visited == set(states) #1 if max_state use, else 0


def generate_TMs(k, parity):
	"""
	k states (+1 including H halting state), 2 symbol (or color) Turing machines
	using k instead of n to disambiguate such from n collatz num
	"""
	states = [chr(ord("A") + i) for i in range(k)]
	states += ["H"] #halt state
	symbols = ["0", "1"]
	dirs = ["L", "R"]

	prods = it.product(symbols, dirs, states)
	#cartesian product to get all machines
	# to develop machines under standard format (e.g. https://www.sligocki.com/2022/10/09/standard-tm-format.html)
	for prod in it.product(prods, repeat = 2*k):
		parts = ["".join(part) for part in prod]# resulting in for ex "1LA"
		# join corresponding parts depending on which state (e.g. A, B, ...) they belong to
		if parts[0][2] == "H" and parts[0][0] == "0":
			continue

		if parts[0][2] == "A":
			continue

		if parity == "even":
			if parts[0][1] == "L": #only for evens
				continue
		elif parity == "odd":
			if parts[0][1] == "R": #only for odds
				continue
		
		if all(part[2] != "H" for part in parts):
		    continue

		if all(part[0] == "0" for part in parts):
			continue

		if all(part[0] == "1" for part in parts):
			#might potentially get rid of some isomorphic machines
			#for n's which are powers of 2
			continue

		state_grouped = ["".join(parts[i*2: (i+1)*2]) for i in range(k)]
		# join all instructions with _ separating instructions respective to different states
		machine = "_".join(state_grouped)

		#skipping machines which have transitions to the same state
		#given an arbitrary state
		if any(part[2] == part[5] for part in state_grouped):
			continue

		#skipping machines which have transitions to the symbol
		#given an arbitrary state
		if any(part[0] == part[3] for part in state_grouped):
			continue


		# skip machines with multiple H transitions (> 1)
		if machine.count("H") > 1:
			continue

		#skip machines which don't make use of all states
		if not TM_max_state_use(machine, k):
			continue

		"""
		need yielding, can't use lists as for 4-state machines
		it's going to be generating on the order of 25*10^9 machines!
		"""
		yield machine

def pickle_TMs(filename, k, parity):
	with gzip.open(filename, "wb") as f:
		for machine in tqdm(generate_TMs(k, parity), desc=f"{k}-state machines", unit="TM"):
			pickle.dump(machine, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	k = 4
	parity = "odd"
	file = f"{k}_state_{parity}.pkl.gz"
	pickle_TMs(file, k, parity)
