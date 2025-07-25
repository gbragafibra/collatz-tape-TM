import numpy as np 
import matplotlib.pyplot as plt 

"""
Want to compare tape development
for a given TM (str format)
and corresponding collatz tape
for a given n
"""

class TM_sim():
	def __init__(self, n, N, machine):
		self.n = n #collatz num
		self.N = N #length of tape
		self.machine = machine #machine in str format (e.g. 1LH0RA_0RB1LA)
	
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

	def sim_TM(self, τ_max = 10**3):
		k = self.machine.count("_") + 1 #state count
		states = [chr(ord("A") + i) for i in range(k)]
		state_transitions = {}
		parts = self.machine.split("_")
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
		τ = frames.shape[0]

		while state != "H" and τ < τ_max:
			symbol = tape[x]
			symbol, dirs, state = state_transitions[state][symbol]
			tape[x] = int(symbol)
			x = (x + (1 if dirs == "R" else -1)) % self.N
			frames = np.concatenate((frames, tape.reshape(1, -1)), axis = 0)
			τ = frames.shape[0]

		return frames

	def compare_TM_collatz(self):
		col_tape = self.collatz_tape()
		TM_tape = self.sim_TM()

		if np.array_equal(col_tape, TM_tape):
			print(f"Machine {self.machine} simulated the collatz tape for n = {self.n}")
		else:
			print(f"Machine {self.machine} didn't simulate the collatz tape for n = {self.n}")

		fig, axs = plt.subplots(1, 2, figsize=(10, 5))

		axs[0].imshow(col_tape, cmap="Greys")
		axs[0].set_title(f"Collatz Tape n = {self.n}")
		axs[0].set_xticks([])
		axs[0].set_yticks([])

		axs[1].imshow(TM_tape, cmap="Greys")
		axs[1].set_title(f"TM Tape {self.machine}")
		axs[1].set_xticks([])
		axs[1].set_yticks([])
		
		for ax in axs:
			for spine in ax.spines.values():
				spine.set_visible(False)

		plt.tight_layout()
		plt.show()


if __name__ == "__main__":
	n = 6
	N = 100
	machine = "1LB0RA_1RC0LA_1RD0RB_1RH0RC"
	sim = TM_sim(n, N, machine)
	sim.compare_TM_collatz()