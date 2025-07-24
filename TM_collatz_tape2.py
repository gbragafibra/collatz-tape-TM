import numpy as np
import itertools as it
from tqdm import tqdm

#num of k state 2-symbol TMs
# as in Radó's "On Non-Computable Functions" (1962) (https://gwern.net/doc/cs/computable/1962-rado.pdf)
TM_num = lambda k: (4 * (k + 1))**(2*k)

class TM_collatz_tape_simulate():
	def __init__(self, n, N):
		self.n = n #collatz num
		self.N = N #tape length
		self.init_par = int(self.n % 2) #initial parity

	def collatz_tape(self):
		S = np.zeros(self.N, dtype="int")
		x = self.N // 2
		dirs = [1, -1]
		frames = S.copy().reshape(1, -1)
		n = self.n
		while n != 1:
			par = int(n % 2) #parity
			if par == 0:
				n /= 2
			else:
				n = 3 * n + 1

			S[x] = 1 - S[x]
			x = (x + dirs[par]) % self.N
			frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)
		return frames #final tape developed; should have (τ + 1, N) dims; τ being stopping time

	def TM_max_state_use(self, machine, k):
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



	def generate_TMs(self, k, skip_counter):
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
				skip_counter["A0_H0"] += 1
				continue

			if parts[0][2] == "A":
				skip_counter["A0_A"] += 1
				continue

			if self.init_par == 0:
				if parts[0][1] == "L": #only for evens
					skip_counter["A0_L"] += 1
					continue
			elif self.init_par == 1:
				if parts[0][1] == "R": #only for odds
					skip_counter["A0_R"] += 1
					continue
			
			if all(part[2] != "H" for part in parts):
			    skip_counter["no_H"] += 1
			    continue

			if all(part[0] == "0" for part in parts):
				skip_counter["all_0"] += 1
				continue

			if all(part[0] == "1" for part in parts):
				#might potentially get rid of some isomorphic machines
				#for n's which are powers of 2
				skip_counter["all_1"] += 1
				continue

			state_grouped = ["".join(parts[i*2: (i+1)*2]) for i in range(k)]

			#skipping machines which have transitions to the same state
			#given an arbitrary state
			if any(part[2] == part[5] for part in state_grouped):
				skip_counter["same_state"] += 1
				continue
			#skipping machines which have transitions to the symbol
			#given an arbitrary state
			if any(part[0] == part[3] for part in state_grouped):
				skip_counter["same_symb"] += 1
				continue

			# join all instructions with _ separating instructions respective to different states
			machine = "_".join(state_grouped)

			# skip machines with multiple H transitions (> 1)
			if machine.count("H") > 1:
				skip_counter["multiple_H"] += 1
				continue

			#skip machines which don't make use of all states
			if not self.TM_max_state_use(machine, k):
				skip_counter["us"] += 1 #unused states
				continue
			"""
			need yielding, can't use lists as for 4-state machines
			it's going to be generating on the order of 25*10^9 machines!
			"""
			yield machine


	def TM_simulate(self):
		col_tape = self.collatz_tape()
		τ = col_tape.shape[0] - 1 #stopping time
		k = 1
		while True:
			skip_counter = {
			"A0_H0": 0,
			"A0_A": 0,
			"no_H": 0,
			"A0_R": 0,
			"A0_L": 0,
			"us": 0, #unused states
			"all_0": 0,
			"all_1": 0,
			"multiple_H": 0,
			"same_state": 0,
			"same_symb": 0
			}
			print(f"Testing {TM_num(k)} machines with {k} state(s)...")
			for machine in tqdm(self.generate_TMs(k, skip_counter), desc=f"{k}-state machines", unit="TM"):
				# get TMs under table format
				states = [chr(ord("A") + i) for i in range(k)]
				state_transitions = {}
				parts = machine.split("_")
				for i, part in enumerate(parts):
					state = states[i]
					state_transitions[state] = {
					0: (part[0], part[1], part[2]),
					1: (part[3], part[4], part[5])
					}
				tape = np.zeros(self.N, dtype="int")
				x = self.N // 2 #init pos
				state = "A" #init state
				frames = tape.copy().reshape(1, -1)

				for i in range(τ):
					if state == "H":
						break
					symbol = tape[x]
					symbol, dirs, state = state_transitions[state][symbol]
					tape[x] = int(symbol)
					x = (x + (1 if dirs == "R" else -1)) % self.N
					frames = np.concatenate((frames, tape.reshape(1, -1)), axis = 0)

					if not np.array_equal(tape, col_tape[i + 1,:]):
						# if tapes differ
						break
				else:
					if state == "H" and frames.shape[0] == τ + 1:
						print(f"Machine {machine} simulated the collatz tape for n = {self.n}")
						return machine
			print(f"Skipped {k}-state machines:")
			for reason, count in skip_counter.items():
				print(f"{reason}: {count}")
			print(f"Done looking for {k}-state machines. Going for {k+1}-state ones.")
			k += 1

		pass




if __name__ == "__main__":
	N = 100 
	n = 8
	collatz_tape_sim = TM_collatz_tape_simulate(n, N)
	collatz_tape_sim.TM_simulate()