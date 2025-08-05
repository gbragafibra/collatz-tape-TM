import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm

class rnd_col():
	def __init__(self, n_max):
		self.n_max = n_max # range (2, n_max) to consider

	def col_stats(self):
		odd_even_ratio = []
		τs = []
		print(fr"Getting collatz stats for n ∈ [2, {self.n_max}]")
		for num in tqdm(range(2, self.n_max), desc = "Collatz ns", unit = "n"):
			n = num 
			τ = 0
			even = 0
			odd = 0
			while n != 1:
				par = int(n % 2) #parity
				if par == 0:
					n /= 2
					even += 1
				else:
					n = 3*n + 1
					odd += 1
				τ += 1
			odd_even_ratio.append(odd/even)
			τs.append(τ)
		return odd_even_ratio, τs
	
	def rnd_tapes(self):
		odd_even_ratios, τs = self.col_stats()
		N = 500 #tape size
		T_ratio = []
		Σ_τ_ratio = []
		for i in tqdm(range(len(odd_even_ratios)), desc = "Random collatz trajectories", unit = "n"):
			ratio, τ = odd_even_ratios[i], τs[i]
			S = np.zeros(N, dtype="int") #init of tape
			visited = np.zeros(N, dtype=bool) #for space(n) func
			x = N // 2 #init pos
			dirs = [1, -1]
			frames = S.copy().reshape(1, -1)
			t = 0
			while t < τ: #run until τ is reached
				r = np.random.random() #num ∈ [0, 1[
				a = ratio/(ratio + 1) #segment related to odds
				if r <= a: par = 1 #like odd
				else: par = 0 #like even
				S[x] = 1 - S[x]
				visited[x] = True
				x = (x + dirs[par]) % N
				frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)
				t += 1
			Σ = np.sum(frames[-1])
			space = np.sum(visited)
			T = "".join(frames[-1].astype(str)) #turn array into str
			T = int(T.strip("0")) #get rid of exterior 0s (0^∞)
			T = int(T) if T else 0 # if "0000" tape for instance
			T_space = int("1" * space) #1^space (in tape compressed format)
			T_ratio.append(T/T_space)
			Σ_τ_ratio.append(Σ/τ)
		return T_ratio, Σ_τ_ratio

if __name__ == "__main__":
	n_max = 50000
	col = rnd_col(n_max)
	T_ratio, Σ_τ_ratio = col.rnd_tapes()
	fig, ax1 = plt.subplots()
	p = ax1.scatter(range(2, n_max), T_ratio, c = Σ_τ_ratio, s = 0.05, cmap = "coolwarm_r")
	cbar = plt.colorbar(p, ax = ax1, label="$Σ/τ$")
	ax1.set_ylabel(r"$T/1^{\text{space(n)}}$")
	ax1.set_xlabel("$n$")
	plt.tight_layout()
	plt.savefig("tape.png", dpi=300, bbox_inches="tight")