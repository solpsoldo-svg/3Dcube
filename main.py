import pygame
import numpy as np
from project_matrix import pj_matrix
from veiw_matrix import veiw
from model_matrix import models_matrix
from normal import normalling

points = np.array([
    [-1, -1, 1, 1],
    [-1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, -1, 1, 1],
    [-1, -1, -1, 1],
    [-1, 1, -1, 1],
    [1, 1, -1, 1],
    [1, -1, -1, 1]
])  # cube's points
index = [
    # front site
    [0, 1, 2],
    [2, 3, 0],
    # right site
    [3, 2, 6],
    [6, 7, 3],
    # left site
    [4, 5, 1],
    [1, 0, 4],
    # bg site
    [6, 5, 4],
    [4, 7, 6],
    # up site
    [7, 4, 0],
    [0, 3, 7],
    # down site
    [1, 5, 6],
    [6, 2, 1],
]  # cube's indexes


def cam_normal(cam_pos, v, normal):  # angle between camera's vector and point's vector

    cam_vec = cam_pos - v
    cam_vec = cam_vec / np.linalg.norm(cam_vec)

    is_normal = np.dot(cam_vec, normal)

    is_normal_deg = np.arccos(is_normal)
    #print(is_normal_deg)

    return np.degrees(is_normal_deg)  # angle


pygame.init()
screen = pygame.display.set_mode((800, 500))

cam_pos = np.array([0, 0, 5])

width, height = screen.get_size()
project_matrix = pj_matrix(0.1, 50.0, width / height, 60)  # near, far, aspect, FOV
veiw_matrix = veiw(np.array([0, 0, 0]), cam_pos, np.array([0, 1, 0]))  # cam_target, cam_pos, vector_up
model = models_matrix(0, 0, 0, 1, 1, 1, 0, 0, 0)  # angleX, angleY, angleZ, sizeX, sizeY, sizeZ, moveX, moveY, moveZ
xv, yv, zv = 0, 0, 0  # start angles

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            quit()
    new_points=[]
    model = models_matrix(0, 0, 0, 1, 1, 1, 0, 0, 0)
    for i in range(len(points)):
        new_points.append(project_matrix @ veiw_matrix @ model @ points[i])
        new_points[i][0], new_points[i][1], new_points[i][2] = new_points[i][0] / new_points[i][3], new_points[i][1] / \
                                                 new_points[i][3], new_points[i][2] / new_points[i][3]
        new_points[i][0], new_points[i][1] = np.round((new_points[i][0] + 1) * width / 2), np.round(
            height - (new_points[i][1] + 1) * height / 2)
    for i in index:
        norm = normalling(new_points[i[0]][:-1], new_points[i[1]][:-1], new_points[i[2]][:-1])
        ang = cam_normal(cam_pos, points[i[1]][:3], norm)
        print(ang)
        if ang > 90:
            continue
        g_color = 200
        pygame.draw.polygon(screen, (g_color, g_color, g_color),
                            [new_points[i[0]][:-2], new_points[i[1]][:-2], new_points[i[2]][:-2]], 1)

    yv += 5
    #xv += 0.001
    pygame.display.flip()
    screen.fill((0, 0, 0))
    pygame.time.wait(40)

