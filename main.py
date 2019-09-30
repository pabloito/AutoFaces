import eigencalculator as ec
import numpy as np

if __name__ == "__main__":
    A = np.random.randn(192, 92)

    a = np.dot(A.T, A)

    EVal, EVec = np.linalg.eig(a)
    for i in range(EVec.shape[1]):
        EVec[:, i] = EVec[:, i] / np.linalg.norm(EVec[:, i])

    eigvals, eigvec = ec.eigen_calc(a, 0.00001)
    print(eigvals, '\n', EVal, '\n', eigvec, '\n', EVec)

