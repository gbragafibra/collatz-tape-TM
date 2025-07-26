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
			n = 3 * n + 1

		S[x] = 1 - S[x]
		visited[x] = True
		x = (x + dirs[par]) % N
		frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)

	τ = frames.shape[0] - 1 #stopping time (without initial empty frame)
	Σ = np.sum(frames[-1])
	space = np.sum(visited)

	T = "".join(frames[-1].astype(str)) #turn array into str
	T = int(T.strip("0")) #get rid of exterior 0s (0^∞)
	T_space = int("1" * space) #1^space (in tape compressed format)
	#print(f"{int(n_init)}; T: {T}; 1^space(n): {T_space}; T_ratio: {T/T_space:.4f}")
	return Σ/τ, T/T_space


if __name__ == "__main__":
	mpmath.mp.dps = 501
	n = 2
	end = n + 100
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 500

	all_res = [collatz_tape(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	Σ_τ_ratio = [res[0] for res in all_res]
	T_ratio = [res[1] for res in all_res]
	"""
	np.set_printoptions(suppress=True)# disable scientific notation
	print(np.unique(T_ratio, return_counts = True))
	"""
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

	p = ax1.scatter(range(len(nums)), T_ratio, c = Σ_τ_ratio, s = 0.05, cmap= "coolwarm_r")
	fig.colorbar(p, ax = ax1, label = "$Σ/τ$")
	ax1.set_ylabel(r"$T/1^{\text{space(n)}}$")
	ax1.set_xlabel("$n$")

	#ax2.hist(T_ratio, bins = 50, color = "darkcyan", edgecolor = "black")
	counts, bins = np.histogram(T_ratio, bins = 200)
	"""#checking for classes of nums (8 classes: 4 classes each with 2 sub-classes)
	for i, count in enumerate(counts):
		if count > 0:
		    bin_start = bins[i]
		    bin_end = bins[i+1]
		    print(f"Bin {i}: [{bin_start:.5f}, {bin_end:.5f}] - {count} entries")
	"""
	relative_freq = counts/counts.sum() 
	
	#classes and respective thresholds
	ε = [[0, 0.005],
	[0.005, 0.01], 
	[0.09, 0.095], 
	[0.095, 0.1], 
	[0.9, 0.905], 
	[0.905, 0.91], 
	[0.99, 0.995], 
	[0.995, 1]]

	classes = [[] for _ in ε]
	for n, T in zip(nums, T_ratio):
		for i, (low, high) in enumerate(ε):
			# need this for last class [0.995, 1]
			if (i < len(ε) - 1 and low <= T < high) or (i == len(ε) - 1 and low <= T <= high):
				classes[i].append(int(n))
				break
	#print(classes)

	ax2.bar(bins[:-1], relative_freq * 100, width = np.diff(bins), align = "edge",
        color = "darkcyan", edgecolor = "black")
	ax2.set_xlabel(r"$T/1^{\text{space(n)}}$")
	ax2.set_ylabel("Relative frequency (%)")

	plt.tight_layout()
	plt.savefig("tape.png", dpi=300, bbox_inches="tight")