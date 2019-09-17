import numpy as np

#
#   Tomo la matriz C que minimiza la dimension.
#   Si A es 15x25 devuelvo C 15x15 en lugar de 25x25.
#
def getSmallestDimensionC(a):
    mat = np.matrix(a)
    m, n = mat.shape
    if m >= n:
        return np.matmul(np.transpose(mat), mat)

    return np.matmul(mat, np.transpose(mat))

def getAllAutoFaces(eigen_vec, images):
    return np.transpose(np.matmul(np.transpose(eigen_vec),images))