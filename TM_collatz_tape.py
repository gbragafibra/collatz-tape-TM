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

	def collatz_tape(self):
		S = np.zeros(self.N, dtype="int")
		x = self.N // 2
		dirs = [1, -1]
		frames = S.copy().reshape(1, -1)
		n = self.n
		while n != 1:
			par = int(n % 2)
			if par == 0:
				n /= 2
			else:
				n = 3 * n + 1

			S[x] = 1 - S[x]
			x = (x + dirs[par]) % self.N
			frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)
		return frames #final tape developed; should have (τ + 1, N) dims; τ being stopping time

	def generate_TMs(self, k):
		"""
		k states (+1 including H halting state), 2 symbol (or color) Turing machines
		using k instead of n to disambiguate such from n collatz num
		"""
		states = [chr(ord("A") + i) for i in range(k)]
		states += ["H"] #halt state
		symbols = ["0", "1"]
		dirs = ["L", "R"]

		prods = list(it.product(symbols, dirs, states)) 
		#cartesian product to get all machines
		# to develop machines under standard format (e.g. https://www.sligocki.com/2022/10/09/standard-tm-format.html)
		for prod in it.product(prods, repeat = 2*k):
			parts = ["".join(part) for part in prod]# resulting in for ex "1LA"
			# join corresponding parts depending on which state (e.g. A, B, ...) they belong to
			state_grouped = ["".join(parts[i*2: (i+1)*2]) for i in range(k)]
			# join all instructions with _ separating instructions respective to different states
			"""
			need yielding, can't use lists as for 4-state machines
			it's going to be generating on the order of 25*10^9 machines!
			"""
			yield "_".join(state_grouped)


	def TM_simulate(self):
		col_tape = self.collatz_tape()
		τ = col_tape.shape[0] - 1 #stopping time
		k = 1
		while True:
			print(f"Testing {TM_num(k)} machines with {k} state(s)...")
			for machine in tqdm(self.generate_TMs(k), desc=f"{k}-state machines", unit="TM"):
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
			print(f"Done looking for {k}-state machines. Going for {k+1}-state ones.")
			k += 1

		pass




if __name__ == "__main__":
	N = 100 
	n = 10
	collatz_tape_sim = TM_collatz_tape_simulate(n, N)
	collatz_tape_sim.TM_simulate()