import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm

def mod4_tape(n, *args):
	S = np.zeros(N, dtype="int")
	visited = np.zeros(N, dtype=bool) #for space(n) func
	x = N // 2
	dirs = [1, -1, -1, 1]
	frames = S.copy().reshape(1, -1)
	n_init = n
	while n != 1:
		par = int(n % 4) #parity
		if par == 0:
			n /= 2
			S[x] = 1 - S[x]
		elif par == 1:
			n = (3*n + 1)/2
			S[x] = 1 - S[x]
		elif par == 2:
			n /= 2
			S[x] = S[x]
		else:
			n = (3*n + 1)/2
			S[x] = S[x]

		visited[x] = True
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)

	Σ = np.sum(frames[-1])
	τ = frames.shape[0]
	T = "".join(frames[-1].astype(str)) #turn array into str
	T = int(T.strip("0")) if T.strip("0") else 0#get rid of exterior 0s (0^∞)
	#T = int(str(T), 2)#to denary
	#print(fr"{int(n_init)}; T: {T}, Σ: {Σ}, T/n: {T/n_init}")
	return T/n_init, Σ/τ
	#return Σ/np.sum(visited), Σ/τ

if __name__ == "__main__":
	mpmath.mp.dps = 201
	n = 2
	end = n + 10**4
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 500
	all_res = [mod4_tape(num) for num in tqdm(nums, desc = "Collatz n", unit = "n")]
	T_ratio = [mpmath.log(res[0]) for res in all_res]
	Σs = [res[1] for res in all_res]
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(len(nums)), T_ratio, c = Σs, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label="$Σ/τ$")
	ax1.set_xlabel("$n$")
	ax1.set_ylabel(r"$\log (T_{10}/n)$")
	plt.tight_layout()
	plt.savefig("tape_T_ratio.png", dpi=300, bbox_inches="tight")