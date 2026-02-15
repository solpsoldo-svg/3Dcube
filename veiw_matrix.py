import numpy as np

def veiw(cam_target, cam_pos, up): # cam_target, cam_pos, vector_up
    cam_z=np.array(cam_target)-np.array(cam_pos)
    cam_z=cam_z/np.linalg.norm(cam_z)

    cam_x=np.cross(up, cam_z)
    cam_x=cam_x/np.linalg.norm(cam_x)

    cam_y=np.cross(cam_z, cam_x)
    cam_y=cam_y/np.linalg.norm(cam_y)

    rotate=np.array([
        [cam_x[0], cam_x[1], cam_x[2], 0],
        [cam_y[0], cam_y[1], cam_y[2], 0],
        [cam_z[0], cam_z[1], cam_z[2], 0],
        [0, 0, 0, 1]
    ])
    tr=np.array([
        [1, 0, 0, -cam_pos[0]],
        [0, 1, 0, -cam_pos[1]],
        [0, 0, 1, -cam_pos[2]],
        [0, 0, 0, 1]
    ])

    return rotate @ tr