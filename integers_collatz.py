import numpy as np
import matplotlib.pyplot as plt 
import mpmath
from tqdm import tqdm
from sympy import prime


#generate alternative integers
def integers():
	n = 1
	while True:
		yield n
		yield -n
		n += 1

class gen_seq():
	def __init__(self):
		self.gen = integers()
		self.sequence = []
	
	def get(self, idx):
		while idx >= len(self.sequence):
			self.sequence.append(next(self.gen))
		return self.sequence[idx]

def trajectory(start_idx):
	seq = gen_seq()
	idx = start_idx

	n = seq.get(idx)
	ns = [n]
	idxs = [idx + 1] #want to see collatz trajectory
	while n != 1:
		idx += n
		n = seq.get(idx)
		ns.append(n)
		idxs.append(idx + 1)
	return ns

def godel_num(vals):
    num = 1
    for i, val in enumerate(vals, start=1):
        num *= mpmath.mpf(prime(i)) ** val
    return num

if __name__ == "__main__":
	mpmath.mp.dps = 5001
	n = 2
	end = n + 100
	nums = [n + int(mpmath.mpf(i)) for i in range(int(end - n))]
	vals = [trajectory(ns) for ns in tqdm(nums, desc = "Collatz n", unit = "n")]
	godel_nums = [godel_num(val) for val in tqdm(vals, desc = "gödel num for n")]
	godel_nums = np.array([float(g) for g in godel_nums])
	plt.plot(range(len(nums)), np.log(godel_nums), "k-")
	plt.show()