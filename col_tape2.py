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

	T = "".join(frames[-1].astype(str)) #turn array into str
	T = T.strip("0") #get rid of exterior 0s (0^∞)
	k = len(T)
	β = 0
	p1 = [i for i in range(len(T)) if int(T[i]) == 1]
	for i in range(Σ - 1):
		β += (2**p1[i]) * (3**(Σ - 1 - i))
	m = β/(2**k - 3**Σ)
	m = 0 if np.isnan(m) else m
	int_status = True if β % (2**k - 3**Σ) == 0 else False 
	return Σ/τ, m, int_status

if __name__ == "__main__":
	mpmath.mp.dps = 101
	n = 2
	end = n + 50000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 200
	all_res = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σ_τ_ratio = [res[0] for res in all_res]
	ms = [res[1] for res in all_res]
	int_status = [res[2] for res in all_res]
	print(np.sum(int_status))
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(len(nums)), ms, c = Σ_τ_ratio, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label="$Σ/τ$")
	ax1.set_ylabel(r"$m$")
	ax1.set_xlabel("$n$")
	plt.tight_layout()
	plt.savefig("tape_m.png", dpi=300, bbox_inches="tight")