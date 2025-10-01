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
	return Σ, Σ/τ

if __name__ == "__main__":
	mpmath.mp.dps = 101
	n = 2
	end = n + 10**6
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 200
	all_res = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σ = [res[0] for res in all_res]
	Σ_τ_ratio = [res[1] for res in all_res]
	fig, ax1 = plt.subplots()
	print(np.argmax(Σ) + n, Σ[np.argmax(Σ)])
	p = ax1.scatter(range(len(nums)), Σ, c = Σ_τ_ratio, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label="$Σ/τ$")
	ax1.set_ylabel(r"$Σ$")
	ax1.set_xlabel("$n$")
	plt.tight_layout()
	plt.savefig("tape_score.png", dpi=300, bbox_inches="tight")