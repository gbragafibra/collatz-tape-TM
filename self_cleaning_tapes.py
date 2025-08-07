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

	τ = frames.shape[0] - 1 #stopping time (without initial empty frame)
	Σ = np.sum(frames[-1])

	return Σ

if __name__ == "__main__":
	mpmath.mp.dps = 501
	n = 3 * 10**6
	end = n + 2 * 10**6
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 200
	Σ = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	print(np.argwhere(np.array(Σ) == 0) + n)
