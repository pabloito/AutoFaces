import numpy as np


"""
Esta implementacion es a partir de un articulo de wikipedia
sobre qr con reflexiones de householder (es original)
"""

##adaptacion de https://en.wikipedia.org/wiki/QR_decomposition#Using_Householder_reflections
def qr_decompa(A):
    rows, cols = A.shape
    # se empieza por Q = I
    Q = np.eye(rows)
    m, n = np.shape(A)
    # todo por ahora se tiene que dar que cols<=rows (igual las matrices de covarianza son cuadradas)
    # la idea es calcular una matriz Hi para cada columna i
    # abajo de la diagonal
    for i in range(n):
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
    haux -= (2 / np.dot(v, v)) * np.outer(v.transpose(), v)
    H[i:, i:] = haux
    return H

## adaptacion de https://www.cs.cornell.edu/~bindel/class/cs6210-f09/lec18.pdf
def qr_decomp(A):
    m, n = np.shape(A)
    Q = np.eye(m)
    R = np.copy(A)
    for i in range(n):
        #guardo la norma (la voy a necesitar mas de una vez...)
        nrm = np.linalg.norm(R[i:m, i])
        u1 = R[i, i] + np.sign(R[i, i]) * nrm
        v = R[i:m, i].reshape((-1, 1)) / u1
        v[0] = 1
        tau = np.sign(R[i, i]) * u1 / nrm
        # Ahorro la multiplicacion de matrices: solo necesito restar una columna de cada matriz
        # Esto en vez de hacer H_i * R
        R[i:m, :] = R[i:m, :] - (tau * v) * np.dot(v.reshape((1, -1)), R[i:m, :])
        # Esto en vez de hacer Q * H_i
        Q[:, i:n] = Q[:, i:n] - (Q[:, i:m].dot(v)).dot(tau * v.transpose())

    return Q, R

def eigen_calc(a, tolerance=0.0001):
    q, r = qr_decomp(a)
    qcomp = q
    condition = True

    i, maxiterations = 0, 50

    while condition and i < maxiterations:
        # [3]
        a = np.matmul(q.transpose(), a)
        a = np.matmul(a, q)
        q, r = qr_decomp(a)
        # [1]
        qcomp = np.matmul(qcomp, q)
        # [2]
        uppertri_eq = np.allclose(a, np.triu(a), atol=tolerance)
        lowertri_eq = np.allclose(a, np.tril(a), atol=tolerance)

        condition = (not lowertri_eq) & (not uppertri_eq)
        condition = True
        i = i+1

    #normalize

    for i in range(0, qcomp.shape[0]):
        qcomp[:, i] = qcomp[:, i] / np.linalg.norm(qcomp[:, i])

    return np.diag(a), qcomp

    #ordeno autovectores en funcion del peso de los autovalores
    a = np.diag(a)

    #argsort es ascendente aplico - para hacerlo descendente.
    sorted_indexes = np.argsort(np.absolute(a))

    eigen_values = a[sorted_indexes]
    eigen_vectors = qcomp[:, sorted_indexes]

    #cada columna de eigen_vectors tiene el autovector correspondiente al autovalor en la misma
    #columna de eigen_values
    return eigen_values, eigen_vectors

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
