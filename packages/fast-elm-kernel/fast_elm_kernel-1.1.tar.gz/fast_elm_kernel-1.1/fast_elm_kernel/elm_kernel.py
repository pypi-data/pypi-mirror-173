import numpy as np

def elm_kernel(X: np.array, Y: np.array):
    """ELM KERNEL -  between two matrices
    Frenay, Parameter-insensitive kernel in extreme learning for non-linear supportvector regression
    Eq. 15
    """
    # here sigma^2 = 1e10 should be large enough to dont add errors
    dSig = 1 / (2 * 1e10)
    # sums per row
    KxDiag = np.sum(X * X, axis=1).reshape((-1, 1))
    KyDiag = np.sum(Y * Y, axis=1).reshape((-1, 1))
    
    return 2 / np.pi * np.arcsin((1 + X @ Y.T) /
                              np.sqrt((dSig + 1 + KxDiag) @ (dSig + 1 + KyDiag).T))
    
def elm_kernel_vec(x: np.array, y: np.array):
    """ELM KERNEL - between two vectors
    Frenay, Parameter-insensitive kernel in extreme learning for non-linear supportvector regression
    Eq. 15
    """
    # here sigma^2 = 1e10 should be large enough to dont add errors
    dSig = 1 / (2 * 1e10)
    # sums per row
    
    return 2 / np.pi * np.arcsin((1 + x @ y) /
                              np.sqrt((dSig + 1 + x @ x) * (dSig + 1 + y @ y).T))