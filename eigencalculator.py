import numpy as np

def qr_decomp(a):
    return np.linalg.qr(a)
    #todo: no se si hace falta que lo implementemos nosotros...
    #
    # m, n = a.shape
    # q = np.zeros((m, n))
    # r = np.zeros((n, n))
    # for j in range(n):
    #     a_j = a[:,j]
    #     for i in range(j):
    #         q_i = q[:,i]
    #         r[i,j] = np.matmul(q_i.T,a_j)
    #         substraction += projection(q[:,i],a_j)
    #     q[:,j]=a_j-substraction

def eigen_calc(a, tolerance=0.0001):
    q, r = qr_decomp(a)
    qcomp = q
    condition = True
    i=0
    while condition:
        print('iteration {}'.format(i))
        i+=1

        #[3]
        a = r*q

        q, r = qr_decomp(a)

        #[1]
        qcomp = np.matmul(qcomp, q)

        #[2]
        uppertri_eq = np.allclose(a, np.triu(a), atol=tolerance)
        lowertri_eq = np.allclose(a, np.tril(a), atol=tolerance)

        condition = (not uppertri_eq) & (not lowertri_eq)

    eigen_values = np.diag(a)
    eigen_vectors = qcomp

    #todo: order eigen_vectors by eigen_values

    return eigen_vectors,eigen_values

#TEST

a = np.matrix('2,1,0;1,2,1;0,1,2')
print(a)
print(eigen_calc(a))


# Tomado de https://en.wikipedia.org/wiki/QR_algorithm
#[1]: For a symmetric matrix A, upon convergence, AQ = QΛ, where Λ is the diagonal matrix of eigenvalues
#   to which A converged, and where Q is a composite of all the orthogonal similarity transforms
#   required to get there. Thus the columns of Q are the eigenvectors.
#[2]: Under certain conditions,[4] the matrices Ak converge to a triangular matrix, the Schur form of A.
#   The eigenvalues of a triangular matrix are listed on the diagonal, and the eigenvalue problem is
#   solved
#[3]: all the Ak are similar and hence they have the same eigenvalues.
#
#
