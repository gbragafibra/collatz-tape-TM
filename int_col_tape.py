import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm


#generate alternative integers
def integers():
	n = 1
	while True:
		yield n
		yield -n
		n += 1

class gen_seq():
	def __init__(self):
		self.gen = integers()
		self.sequence = []
	
	def get(self, idx):
		while idx >= len(self.sequence):
			self.sequence.append(next(self.gen))
		return self.sequence[idx]

def tape(start_idx):
	N = 200 # tape length
	S = np.zeros(N, dtype="int")
	x = N // 2
	frames = S.copy().reshape(1, -1)
	dirs = [1, -1]
	seq = gen_seq()
	idx = int(start_idx)

	n = seq.get(idx)
	while n != 1:
		par = int(n % 2)
		S[x] = 1 - S[x]
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)
		idx += n
		n = seq.get(idx)
	Σ = np.sum(frames[-1])
	τ = frames.shape[0] - 1
	return Σ/τ

if __name__ == "__main__":
	mpmath.mp.dps = 101
	n = 1 
	end = n + 50000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))] #idxs
	all_res = [tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	#Σ_τ_ratio = [res[0] for res in all_res]
	plt.plot(range(len(nums)), all_res, "k.")
	plt.show()