import pygame
import numpy as np
from project_matrix import pj_matrix
from veiw_matrix import veiw
from model_matrix import models_matrix
from normal import normalling
from clipping import clip

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


def cam_normal(campos, v, normal):  # angle between camera's vector and point's vector

    cam_vec = campos - v
    cam_vec = cam_vec / np.linalg.norm(cam_vec)

    is_normal = np.clip(np.dot(cam_vec, normal), -1.0, 1.0)

    is_normal_deg = np.arccos(is_normal)

    return np.degrees(is_normal_deg)  # angle


pygame.init()
screen = pygame.display.set_mode((800, 500))

cam_pos = np.array([0, 0, 2])
target_pos = np.array([0, 0, 1])

cam_target_vec = np.array(target_pos - cam_pos)
cam_target_vec = np.array(cam_target_vec/np.linalg.norm(cam_target_vec))

width, height = screen.get_size()

pygame.mouse.set_pos(width // 2, height // 2)#mouse pos
is_tab = False

project_matrix = pj_matrix(0.1, 50.0, width / height, 60)  # near, far, aspect, FOV

xv, yv, zv = 0, 0, 0  # start angles
angle_target = 0 #start angle rotate target_pos around cam_pos
angy = 0
vector_up = np.array([0, 1, 0])

new_angle_target = np.radians(angle_target)
ct, st = np.cos(new_angle_target), np.sin(new_angle_target)

new_angy = np.radians(angy)
yc, ys = np.cos(new_angy), np.sin(new_angy)

lastpos = np.array([0, 0])

pos = np.array([0, 0])

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ex = pygame.QUIT
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if is_tab:  is_tab = False; pygame.mouse.set_visible(True)
                else:   is_tab = True; pygame.mouse.set_visible(False)

        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pos() != (width // 2, height //2) and is_tab:

            m_x, m_y = pygame.mouse.get_rel()

            angle_target += m_x // 3
            if angle_target >= 360 or angle_target <= -360:
                angle_target = 0
            new_angle_target = np.radians(angle_target)
            ct, st = np.cos(new_angle_target), np.sin(new_angle_target)

            angy += m_y // 3
            if angy >= 360 or angy <= -360:
                angy = 0
            new_angy = np.radians(angy)
            yc, ys = np.cos(new_angy), np.sin(new_angy)



            target_pos = np.array([ct * yc, ys, st * yc]) + cam_pos

            cam_target_vec = np.array(cam_pos - target_pos)
            cam_target_vec = cam_target_vec / np.linalg.norm(cam_target_vec)

            print(cam_target_vec * np.linalg.norm(cam_target_vec))

        keys = pygame.key.get_pressed()
        if is_tab:
            if keys[pygame.K_w]:
                cam_pos = cam_pos - cam_target_vec
                target_pos = target_pos - cam_target_vec
            if keys[pygame.K_s]:
                cam_pos = cam_pos + cam_target_vec
                target_pos = target_pos + cam_target_vec

            vc = np.cross(np.array([cam_target_vec[0], 0, cam_target_vec[2]]), vector_up)
            if np.linalg.norm(vc) != 0:
                vc = vc / np.linalg.norm(vc)

                if keys[pygame.K_d]:
                    cam_pos = cam_pos - vc
                    target_pos = target_pos - vc

                if keys[pygame.K_a]:
                    cam_pos = cam_pos + vc
                    target_pos = target_pos + vc

    if is_tab:  pygame.mouse.set_pos(width // 2, height // 2)

    new_points = []
    newp = []
    veiw_matrix = veiw(target_pos, cam_pos, vector_up) # cam_target, cam_pos, vector_up
    model = models_matrix(0, yv, 0, 1, 1, 1, 0, 0, 0) # angleX, angleY, angleZ, sizeX, sizeY, sizeZ, moveX, moveY, moveZ
    for i in range(len(points)):
        newp.append(model @ points[i])
        new_points.append(project_matrix @ veiw_matrix @ model @ points[i])
        if new_points[i][3] != 0:
            new_points[i][0], new_points[i][1], new_points[i][2] = new_points[i][0] / new_points[i][3], new_points[i][1] / new_points[i][3], new_points[i][2] / new_points[i][3]
        new_points[i][0], new_points[i][1] = np.round((new_points[i][0] + 1) * width / 2), np.round(
            height - (new_points[i][1] + 1) * height / 2)
    for i in index:
        norm = normalling(newp[i[0]][:-1], newp[i[1]][:-1], newp[i[2]][:-1])
        ang = cam_normal(cam_pos, newp[i[1]][:3], norm)
        ang1 = cam_normal(cam_pos, target_pos, norm)

        aaa, normal1 = cam_pos - target_pos, cam_pos - newp[i[1]][:3]
        is_normal1 = np.clip(np.dot(aaa , normal1), -1.0, 1.0)
        is_normal_deg1 = np.degrees(np.arccos(is_normal1))

        if ang <= 90 and is_normal_deg1 <= 90:
            temp_arr2 = []
            temp_arr1 = []
            if 0 < new_points[i[0]][:-2][0] < width and 0 < new_points[i[0]][:-2][1] < height:
                temp_arr1.append(new_points[i[0]][:-2])
            if 0 < new_points[i[1]][:-2][0] < width and 0 < new_points[i[1]][:-2][1] < height:
                temp_arr1.append(new_points[i[1]][:-2])
            if 0 < new_points[i[2]][:-2][0] < width and 0 < new_points[i[2]][:-2][1] < height:
                temp_arr1.append(new_points[i[2]][:-2])

            if not(0 < new_points[i[0]][:-2][0] < width) or not(0 < new_points[i[0]][:-2][1] < height):
               temp_arr2.append(new_points[i[0]][:-2])
            if not(0 < new_points[i[1]][:-2][0] < width) or not(0 < new_points[i[1]][:-2][1] < height):
                temp_arr2.append(new_points[i[1]][:-2])
            if not(0 < new_points[i[2]][:-2][0] < width) or not(0 < new_points[i[2]][:-2][1] < height):
                temp_arr2.append(new_points[i[2]][:-2])

            g_color = 255 - int(ang1) // 2
            pygame.draw.polygon(screen, (g_color, 0, g_color),
                            [new_points[i[0]][:-2], new_points[i[1]][:-2], new_points[i[2]][:-2]])
    #yv += 5
    pygame.display.flip()
    screen.fill((0, 0, 0))
    pygame.time.wait(40)
