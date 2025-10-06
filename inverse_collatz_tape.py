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
	return Σ, Σ/τ


if __name__ == "__main__":
	mpmath.mp.dps = 201
	n = 2
	end = n + 10**6
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 400
	all_res = [collatz_tape(num) for num in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σs = np.array([res[0] for res in all_res])
	Σ_ratio = [res[1] for res in all_res]
	n_Σs = [np.log(np.argwhere(Σs == k)[0] + n) for k in range(0, 38, 1)]
	Σ_ratio = [Σ_ratio[int(idx - n)] for idx in n_Σs]
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(len(n_Σs)), n_Σs, c = Σ_ratio, s = 1, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label="$Σ/τ$")
	ax1.set_xlabel("$Σ$")
	ax1.set_ylabel(r"$\log(n)$")
	plt.tight_layout()
	plt.savefig("inverse_col_tape.png", dpi=300, bbox_inches="tight")