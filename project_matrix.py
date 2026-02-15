import numpy as np

def pj_matrix(n, f, aspect, a): # near, far, aspect, FOV
    a=(a*np.pi)/180
    t = n*np.tan(a/2)
    b = -t
    r = t*aspect
    l = -r
    return np.array([
        [2 * n / (r - l), 0, (r + l) / (r - l), 0],
        [0, 2 * n / (t - b), (t + b) / (t - b), 0],
        [0, 0, -(f + n) / (f - n), -2 * f * n / (f - n)],
        [0, 0, -1, 0]
    ])