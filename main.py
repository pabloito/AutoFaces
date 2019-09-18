import eigencalculator as ec
import numpy as np

if __name__ == "__main__":
    A = np.random.randn(3, 3)
    a = np.array([[2, 1, 0],
                  [1, 2, 1],
                  [0, 1, 2]])

    print(np.linalg.eigvals(a))
    eigvec, eigvals = ec.eigen_calc(a, 0.00000001)
    print(eigvals)

