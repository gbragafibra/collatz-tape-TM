import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm

def collatz_tape(n, *args):
	S = np.zeros(N, dtype="int")
	x = N // 2
	dirs = [1, -1]
	frames = S.copy().reshape(1, -1)
	n_init = n
	while n != 1:
		par = int(n % 2) #parity
		if par == 0:
			n /= 2
		else:
			n = (3 * n + 1)/2
		S[x] = 1 - S[x]
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)

	Σ = np.sum(frames[-1])
	τ = frames.shape[0]
	T = "".join(frames[-1].astype(str)) #turn array into str
	T = int(T.strip("0")) if T.strip("0") else 0#get rid of exterior 0s (0^∞)
	return T

def TM_str(T, k = 3):
	"""
	k is num of bits allocated to state description
	e.g. k = 3: 000 -> A, 001 -> B, ...
	"""
	T = str(T)
	"""
	2 bits for symbol and dir description:
	0 -> 0, 1 -> 1
	0 -> L, 1 -> R
	Want to partition T by block_size
	"""
	block_size = 2 + k
	n_blocks = len(T) // block_size
	r = len(T) % block_size
	n_states = (n_blocks + 1) // 2
	#initialize instructions
	inst = {chr(ord("A") + i): ["---","---"] for i in range(n_states)}

	"""
	generate state map decoding
	e.g. 000 -> A, etc
	"""
	state_map = {}
	for i in range(2**k):
		#i to bin str with k bits
		bits = format(i, f"0{k}b")
		state_map[bits] = chr(ord("A") + i)

	for i in range(n_blocks):
		block = T[i * block_size: (i + 1) * block_size]
		symb_bit = block[0]
		dir_bit = block[1]
		state_bits = block[2: 2+k]
		state = state_map[state_bits]

		#2 instructions per state for state idx and symb idx
		# inst[state idx][sym idx]
		inst[chr(ord("A") + i // 2)][i % 2] = f"{symb_bit}{'L' if dir_bit == '0' else 'R'}{state}"

	# dealing with last part of T
	#which potentially might not have
	#been partitioned
	if r != 0:
		block = T[n_blocks * block_size:]
		state = chr(ord("A") + n_blocks // 2)
		sym_idx = n_blocks % 2

		if state not in inst:
			inst[state] = ["---", "---"]

		tr = f"{block[0]}" #starting with symb

		if len(block) >= 2: #tackle dir bits
			tr += "L" if block[1] == "0" else "R"
		else:
			tr += "-" #undefined

		if len(block[2:]) != k:
			tr += "-"

		inst[state][sym_idx] = tr

	tm_str = "_".join(["".join(inst[s]) for s in sorted(inst.keys())])
	return tm_str


if __name__ == "__main__":
	mpmath.mp.dps = 201
	#n = mpmath.mpf("1e150")
	n = 2
	end = n + 100
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 5000
	for num in nums:
		T = collatz_tape(num)
		print(T, TM_str(T))