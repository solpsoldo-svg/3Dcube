import numpy as np
import math
def models_matrix(xa, ya, za, sax, say, saz, tx, ty, tz): # angleX, angleY, angleZ, sizeX, sizeY, sizeZ, moveX, moveY, moveZ
    xa = np.radians(xa)
    ya = np.radians(ya)
    za = np.radians(za)
    cx=np.cos(xa)
    sx=np.sin(xa)
    cy = np.cos(ya)
    sy = np.sin(ya)
    cz = np.cos(za)
    sz = np.sin(za)
    x_mat=np.array([
        [1, 0, 0, 0],
        [0, cx, -sx, 0],
        [0, sx, cx, 0],
        [0, 0, 0, 1]
    ])
    y_mat=np.array([
        [cy, 0, sy, 0],
        [0, 1, 0, 0],
        [-sy, 0, cy, 0],
        [0, 0, 0, 1]
    ])
    z_mat=np.array([
        [cz, -sz, 0, 0],
        [sz, cz, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    rotate_matrix = x_mat @ y_mat @ z_mat
    size_mat=np.array([
        [sax, 0, 0, 0],
        [0, say, 0, 0],
        [0, 0, saz, 0],
        [0, 0, 0, 1]
    ])
    translate_mat=np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

    return translate_mat @ rotate_matrix @ size_mat