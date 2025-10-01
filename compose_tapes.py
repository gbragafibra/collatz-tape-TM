import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm
import random

def compose_tapes(*args):
	Σs = []
	Σs_τ = []
	S = np.zeros(N, dtype="int")
	visited = np.zeros(N, dtype=bool)
	x = N // 2
	dirs = [1, -1]
	τ = 0
	for n in tqdm(nums, desc = "Collatz n", unit = "n"):
		while n != 1:
			par = int(n % 2) #parity
			if par == 0:
				n /= 2
			else:
				n = (3 * n + 1)/2
			visited[x] = True
			S[x] = 1 - S[x]
			x = (x + dirs[par]) % N
			τ += 1
		Σs.append(np.sum(S)/np.sum(visited))
		Σs_τ.append(np.sum(S)/τ)

	return Σs, Σs_τ

if __name__ == "__main__":
	mpmath.mp.dps = 501
	n = 2
	end = n + 10000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	#random.seed(37)
	#random.shuffle(nums)

	N = 100000
	all_res = [compose_tapes(nums)]
	Σs = [res[0] for res in all_res]
	Σs_τ = [res[1] for res in all_res]
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(len(nums)), Σs, c = Σs_τ, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label = r"$Σ(n)/τ_{n}$")
	ax1.set_xlabel("$n$")
	ax1.set_ylabel(r"$Σ(n)/\text{space}(n)$")
	plt.tight_layout()
	plt.savefig("tape_compose.png", dpi=300, bbox_inches="tight")