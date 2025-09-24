import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm

class recursive_tape():
	def __init__(self, n, N):
		self.n = n #init collatz num
		self.N = N #tape's length

	def collatz_tape(self, num):
		S = np.zeros(self.N, dtype = "int")
		x = self.N // 2
		dirs = [1, -1]
		frames = S.copy().reshape(1, -1)
		n = num #can be either self.n or T from compose()
		while n != 1:
			par = int(n % 2)
			if par == 0:
				n /= 2
			else:
				n = (3*n + 1)/2
			S[x] = 1 - S[x]
			x = (x + dirs[par]) % self.N
			frames = np.concatenate((frames, S.reshape(1, -1)), axis = 0)
		T = "".join(frames[-1].astype(str))#turn array into str
		T = int(T.strip("0")) if T.strip("0") else 0#get rid of exterior 0s (0^∞)
		T = int(str(T), 2) #turn into denary
		return T

	def compose(self):
		seen = {} #dict for loop checking
		T = self.collatz_tape(self.n)
		k = 0
		while True:
			if T in seen:
				loop_start = seen[T]
				β = k - loop_start #loop's length
				return ("loop", β)

			seen[T] = k
			if T == 0: return ("halt", k)
			T = self.collatz_tape(T)
			k += 1

if __name__ == "__main__":
	mpmath.mp.dps = 501
	n = 6
	end = n + 10000
	nums = [n + mpmath.mpf(i) for i in range(int(end - n))]
	N = 2000

	halts_x, halts_y = [], []
	loops_x, loops_y = [], []

	for num in tqdm(nums, desc = "Collatz n", unit = "n"):
		tape = recursive_tape(num, N)
		result, value = tape.compose()
		if result == "halt":
			halts_x.append(num)
			halts_y.append(value)
		else:
			loops_x.append(num)
			loops_y.append(value)

	fig, ax = plt.subplots()
	ax.scatter(halts_x, halts_y, color="blue", marker = ".", label="Halts (depth $k$)")
	ax.scatter(loops_x, loops_y, color="red", marker="*", label="Loops (length $β$)")
	ax.set_xlabel("$n$")
	ax.set_ylabel("$k$ or $β$")
	ax.legend()
	plt.tight_layout()
	plt.show()