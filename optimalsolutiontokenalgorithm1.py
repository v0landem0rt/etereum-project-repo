import numpy as np
import heapq
import math

class Discrete:
    def __init__(self, A0, N0, k0): #переменные, которые мы подаем на вход
        self.A = A0
        self.N = N0
        self.k = k0


    def preprocess(self):
        a_star = self.A
        k = self.k
        largest_ele_index = heapq.nlargest(k-1, range(len(a_star)), key=a_star.__getitem__)
        sum_ar = 0
        length_ar = len(a_star)
        M = np.sum(a_star)/k
        for i in range(0, length_ar):
            if i not in largest_ele_index:
                sum_ar = sum_ar + np.sum(a_star[i])
        B = 0
        start = self.N - self.k+1
        n = 2
        A = a_star
        for start in range(start,self.N):
            a_star_inner = a_star
            A_NKn = A[self.N-self.k+n-1]
            index_S_inner = self.N-self.k+n-1
            index_a_inner = self.N-self.k+n
            S_inner = np.sum(a_star[0:index_S_inner])
            if S_inner/(n-1) >= A_NKn:
                a_star_res = a_star_inner
                a_star_res[self.N-self.k+n-1] = A[self.N-self.k+n-1]
                sum_ar = sum_ar + a_star_res[index_S_inner]
            else:
                a_star_Nkn = math.floor(S_inner/(n-1))
                max_ele_in_A = np.max(largest_ele_index)
                delta = abs(math.floor(A[index_S_inner]-a_star_Nkn))
                a_star_res[self.N-self.k+n-1] = a_star_Nkn
                B = B + delta
                sum_ar = sum_ar + a_star_res[index_S_inner]
            n = n+1
        return a_star_res, B


    def distribution(self, a_star_res, B):
        print("-------------------------")
        S = np.sum(a_star_res)
        M_star = math.floor(S/self.k)
        B0 = abs(S - M_star*self.k)
        n = self.N - B0 +1 # n = N - B0
        for n in range(n, self.N+1):
            a_star_res[n-1] = a_star_res[n-1] - 1
            B = B + B0
        I_n = np.zeros(self.N+1)
        r_n = np.zeros(self.N+1)
        for n in range(1,self.N+1):
            I_n[n] = np.sum(a_star_res[0:n-1])+1
            r_n[n] = np.sum(a_star_res[0:n])
        my_matrix = np.zeros((self.k, M_star))
        n = 1
        for i in range(1, M_star + 1):
            for j in range(1, self.k+1):
                check_index = i + M_star * (j - 1)
                for n in range(1, self.N+1):
                    if check_index <= r_n[n] and check_index >= I_n[n]:
                        my_matrix[j-1, i-1] = n
                    n =n+1
        #print("optimal tokenization by algorithm 1 is\n", my_matrix)
        return my_matrix.T 


if __name__ == "__main__":
    A = np.array([3,4,3,5,8,2]) #np.array([1,1,3,4,6])
    N = len(A)
    k = 3
    my_res_1 = Discrete(A, N, k)
    res_1, my_B= my_res_1.preprocess()
    print(f'a_star is {res_1}\nB is {my_B}')
    res_distri = my_res_1.distribution(res_1, my_B)
    print('res distri',res_distri)
