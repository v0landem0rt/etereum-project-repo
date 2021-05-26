import numpy as np
from sympy import symbols, solve, Eq

class Continuous:
    def __init__(self, N0, A0, target_var_reduc):
        self.A = A0
        self.N = N0
        self.var = target_var_reduc

    def search(self):
        E = 0
        V = 0
        a_n = np.zeros(self.N)
        N = self.N
        A = self.A
        var = self.var
        A = np.insert(A, 0, 0)
        print("A is ",A)
        for n in range(0, N):
            E_new = E + (N-n)*(A[n+1] - A[n])
            V_new = V + (N-n)*(A[n+1]**2 - A[n]**2)
            check = (1/var)*(E_new)**2
            if check >= V_new:
                E = E_new
                V = V_new
                for k in range(n+1-1, N):
                    a_n[k] = A[n+1]
                # print("a_n = ", a_n)
                # print(f'E = {E} and V = {V}')
            else:
                x = symbols('x')
                E_new = E + (N-n)*(A[n+1] - A[n])
                expr = (1/var)*(E_new + (N - n)*(x - A[n+1]))**2 - V + (N - n) * (x**2 - A[n+1]**2)
                A_sol = solve(expr)
                A_sol_positive =  [i for i in A_sol if i > 0]
                A_sol = A_sol_positive[0]
                E = E + (N-n)*(A_sol - A[n])
                V = V + (N-n)*(A_sol**2 - A[n]**2)
                n_star = n + 1
                for k in range(n_star-1, N):
                    a_n[k] = A_sol
                # print("a_n = ",a_n)
                # print(f'E = {E} and V = {V}')
        return a_n

    def construct_pack(self, a_n):
        M = np.linalg.norm((a_n), ord=1)
        # print("norm L1 is", M)
        composition  = a_n/M
        return  composition


if __name__ == "__main__":
    A = np.array([3,4,5])
    N = len(A)

    my_var = np.var(A)
    length = len(A)
    my_min = np.min(A)
    my_max = np.max(A)
    rand1 = np.random.randint(my_min, my_max + 1, size=length)
    rand2 = np.random.randint(my_min, my_max + 1, size=length)
    cov_rand = np.cov(rand1, rand2)[0, 0]
    var_red = cov_rand/my_var

    my_res_1 = Continuous(N, A, var_red)
    res_1 = my_res_1.search()
    print("final a_n = ", res_1)
    res_2 = my_res_1.construct_pack(res_1)
    print("composition is", res_2)
