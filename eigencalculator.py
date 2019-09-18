import numpy as np


"""
Esta implementacion es a partir de un articulo de wikipedia
sobre qr con reflexiones de householder (es original)
"""
def qr_decomp(A):
    rows, cols = A.shape
    # se empieza por Q = I
    Q = np.eye(rows)
    # todo por ahora se tiene que dar que cols<=rows (igual las matrices de covarianza son cuadradas)
    # la idea es calcular una matriz Hi para cada columna i
    # abajo de la diagonal
    for i in range(cols - (rows == cols)):
        # se calcula H_i, la matriz que multiplicando a A por izquierda
        # vuelve nulos los elementos bajo la diagonal en la columna i
        H_i = calculate_ith_h(A[i:, i], rows, i)
        # se supone que la matriz Q al final sea I*H0*H1*H2...*Hcols-1 (o Hcols-2, si rows==cols)
        Q = np.dot(Q, H_i)
        # A al final es una matriz triangular superior, que cumple
        # A(final) = R =  Hcols-(rows==cols) * ... * H2 * H1 * H0 * A(inicial)
        A = np.dot(H_i, A)
    return Q, A

def calculate_ith_h(a, rows, i):
    H = np.eye(rows)
    # Se calcula haux = Identidad - 2/(dot(v,v'))*(v'v)
    e = np.zeros(a.shape[0])
    e[0] = 1
    u = a + np.copysign(np.linalg.norm(a), a[0]) * e
    v = u / u[0]
    # la H sub i es haux "embebida" en una matriz identidad
    haux = np.eye(a.shape[0])
    haux -= (2 / np.dot(v, v)) * np.outer(np.array(v), np.array(v))
    H[i:, i:] = haux
    return H

#def qr_decomp:
    #return np.linalg.qr(a)
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


    #ordeno autovectores en funcion del peso de los autovalores
    a = np.diag(a)

    #argsort es ascendente aplico - para hacerlo descendente.
    sorted_indexes = (-a).argsort()

    eigen_values = a[sorted_indexes]
    eigen_vectors = qcomp[:,sorted_indexes]

    #cada columna de eigen_vectors tiene el autovector correspondiente al autovalor en la misma
    #columna de eigen_values
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
