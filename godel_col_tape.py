import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm
from sympy import prime

def collatz_tape(n, *args):
	S = np.zeros(N, dtype="int")
	x = N // 2
	dirs = [1, -1]
	frames = S.copy().reshape(1, -1)
	n_init = n
	visited = np.zeros(N, dtype=bool) #for space(n) func
	while n != 1:
		par = int(n % 2) #parity
		if par == 0:
			n /= 2
		else:
			n = 3 * n + 1

		S[x] = 1 - S[x]
		visited[x] = True
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)

	τ = frames.shape[0] - 1 #stopping time (without initial empty frame)
	Σ = np.sum(frames[-1])
	space = np.sum(visited)

	T = "".join(frames[-1].astype(str)) #turn array into str
	T = T.strip("0") #get rid of exterior 0s (0^∞)
	T_space = "1" * space #1^space (in tape compressed format)
	
	symbol_map = {
	"0": 1,
	"1": 2
	}
	vals_T = [symbol_map[t] for t in T]
	φ_T = 1 #gödel num
	for i, val in enumerate(vals_T, start=1):
		φ_T *= prime(i) ** val

	vals_space = [symbol_map[t] for t in T_space]
	φ_space = 1 
	for i, val in enumerate(vals_space, start=1):
		φ_space *= prime(i) ** val
	return Σ/τ, φ_T/φ_space #,φ_T 

if __name__ == "__main__":
	mpmath.mp.dps = 1001
	n = 2
	end = n + 1000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 500

"""
	φ_old = collatz_tape(5)
	k = 2
	for _ in range(k):
		φ = collatz_tape(φ_old)
		print(φ/φ_old)
		φ_old = φ
"""
	all_res = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σ_τ_ratio = [res[0] for res in all_res]
	φs = [res[1] for res in all_res]

	p = plt.scatter(range(len(nums)), φs, c = Σ_τ_ratio, s = 0.05, cmap= "coolwarm_r")
	plt.colorbar(p, label = "$Σ/τ$")
	plt.ylabel(r"$\varphi(T)/\varphi(1^{\text{space(n)}})$")
	plt.xlabel("$n$")
	plt.tight_layout()
	plt.savefig("godel_tape.png", dpi=300, bbox_inches="tight")