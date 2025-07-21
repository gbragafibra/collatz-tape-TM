# collatz-tape-TM

Consider an empty tape with all unmarked cells, such that the reading head (standing initially in the middle of the tape) applies the collatz function to a starting $n$:

$$
f(n) = \begin{cases}
n/2 & \text{if} \quad n \equiv 0 \quad (\text{mod}\, 2) \\
3n + 1 & \text{if} \quad n \equiv 1 \quad (\text{mod}\, 2) \\
\end{cases}
$$

flipping the state of the cell it currently stands in, and then moving left if $n$ is odd, and right if $n$ is even. It will do this until $n = 1$ is reached. Consider the example of $n = 5$:

![](/misc_data/collatz_tape5.gif)

and the corresponding tape development over time ($\downarrow$):

![](/misc_data/developed_collatz_tape5.png)

What is the smallest k-state 2-symbol Turing machine (TM) which simulates such tape development? It is the following 3-state machine `1LB0LA_1RC0LA_1LH0RB` (in corresponding string format and according to standard TM notation - as for instance described in this [blog post](https://www.sligocki.com/2022/10/09/standard-tm-format.html)). There can of course be other isomorphic machines which will have the same behaviour, but our interest resides much more in determining the minimum k for which simulation of the collatz tape is achieved (and how k depends on the corresponding collatz numbers n). Additionally, the usual notation for TMs is that of n-state k-symbol (or color) TMs, however since we're restricting our analysis to 2 symbols, and since there's already the use of n to refer to the corresponding collatz number, the number of states will thereby be referred to as k. 

Let's consider some of the already determined machines for from $n = 2$ to $n = 10$ (and some of those which will require better search processes, i.e. non-naïve ones):

|$n$| Machine |
|---|---|
|2|`1LH0LA`|
|3|$k ≥ 4$|
|4|`1RB0LA_1LH0LA`|
|5|`1LB0LA_1RC0LA_1LH0RB`|
|6|$k ≥ 4$|
|7|$k ≥ 4$|
|8|`1RB0LA_1RC0LA_1LH0LA`|
|9|$k ≥ 4$|
|10|$k ≥ 4$|

A first aspect which is trivial is that powers of 2 will be simulated by k-state TMs, according to the relationship $k(n) = 2^{k}$ if $(n & (n - 1)) == 0$ for $n > 0$, with $&$ being the bitwise AND operator. So the next power of 2, $n = 16$, will be simulated by a 4-state TM.

Another remark (of things to do) is to search in a better manner for such machines. The exclusion of isomorphic machines along with non-sensical (ones which halt at the start) that will never be able to simulate a collatz tape, should be considered as the search space for machines with 4-states has the size of 25600000000. The size of the search space for k-state 2-symbol TMs being:

$$
N(k) = (4(k + 1))^{2k}
$$

as present in [Radós "On Non-Computable Functions" (1962) paper](https://gwern.net/doc/cs/computable/1962-rado.pdf).