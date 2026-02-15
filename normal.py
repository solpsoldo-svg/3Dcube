import numpy as np


def normalling(v1, v2, v3): # point1, point2, point3
    edge1 = v2 - v1
    edge2 = v2 - v3

    normal = np.cross(edge1, edge2)

    return normal / np.linalg.norm(normal)
