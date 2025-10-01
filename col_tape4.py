import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm

def collatz_tape(n, *args):
	S = np.zeros(N, dtype="int")
	visited = np.zeros(N, dtype=bool) #for space(n) func
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
		visited[x] = True
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)

	τ = frames.shape[0] - 1 #stopping time (without initial empty frame)
	Σ = np.sum(frames[-1])

	return Σ/np.sum(visited), Σ/τ

if __name__ == "__main__":
	mpmath.mp.dps = 501
	n = 2
	end = n + 10000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 500
	all_res = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σ_space = [res[0] for res in all_res]
	Σ_τ = [res[1] for res in all_res]
	print(np.sum(np.array(Σ_space) == 0.5)/len(Σ_space))
	"""
	min_freq = np.sum(np.array(Σ_space) < 0.5)/len(Σ_space)
	max_freq = np.sum(np.array(Σ_space) > 0.5)/len(Σ_space)
	min_mean = np.mean(np.array(Σ_space).ravel()[np.array(Σ_space).ravel() < 0.5])
	max_mean = np.mean(np.array(Σ_space).ravel()[np.array(Σ_space).ravel() > 0.5])
	print(min_freq, min_mean)
	print(max_freq, max_mean)
	"""
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(len(nums)), Σ_space, c = Σ_τ, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label = r"$Σ(n)/τ_{n}$")
	ax1.set_xlabel("$n$")
	ax1.set_ylabel(r"$Σ(n)/\text{space}(n)$")
	plt.tight_layout()
	plt.savefig("tape_space.png", dpi=300, bbox_inches="tight")
