import numpy as np
from typing import Tuple

coup = int
vbf = np.ndarray
ti = np.ndarray
x = np.ndarray
y = np.ndarray
z = np.ndarray

# Table
ht = 76e-2 # hauteur de la table
Lt = 2.74 # longueur de la table
lt = 1.525 # largeur de la table

# Filet
hf = 15.25e-2 # hauteur du filet
lf = 1.83 # largeur du filet

# Balle
mb = 2.74e-3 # masse de la balle
Rb = 1.99e-2 # rayon de la balle

def Devoir2(option: int, rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> Tuple[coup, vbf, ti, x, y, z]:
    q = q0(rbi, vbi, wbi)
    t = 0 # t0
    dt = 0.01 # delta t


def q0(rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> np.ndarray:
    q = np.zeros(18)

    q[0] = vbi[0] # vx
    q[1] = vbi[1] # vy
    q[2] = vbi[2] # vz
    q[3] = rbi[0] # x
    q[4] = rbi[1] # y
    q[5] = rbi[2] # z
    q[6] = wbi[0] # wx
    q[7] = wbi[1] # wy
    q[8] = wbi[2] # wz
    q[9] = 1 # Rxx
    q[13] = 1 # Ryy
    q[17] = 1 # Rzz

    return q

def toucheSol(q0: np.ndarray, q1: np.ndarray) -> bool:
    z0 = q0[5] # z précédent
    z1 = q1[5] # z actuel

    return z0 > 0 + Rb and z1 <= 0 + Rb # si la balle traverse le sol en z

def toucheFilet(q0: np.ndarray, q1: np.ndarray) -> bool:
    x0 = q0[3] # x précédent
    x1 = q1[3] # x actuel
    y0 = q0[4] # y précédent
    y1 = q1[4] # y actuel
    z0 = q0[5] # z précédent
    z1 = q1[5] # z actuel

    cond_x = x0 < lf/2 - Rb and x1 >= lf/2 - Rb # si la balle traverse le filet en x
    cond_y = (-lf/2 - Rb) <= y0 <= (lf/2 + Rb) and (-lf/2 - Rb) <= y1 <= (lf/2 + Rb) # si la balle est dans le filet en y
    cond_z = (ht + Rb) <= z0 <= (ht + hf) and (ht + Rb) <= z1 <= (ht + hf) # si la balle est dans le filet en z

    return cond_x and cond_y and cond_z

def RungeKutta4(q: np.ndarray, t: int, dt: int, g: np.ndarray) -> np.ndarray:
    k1 = g(q, t)
    k2 = g(q + dt/2 * k1, t + dt/2)
    k3 = g(q + dt/2 * k2, t + dt/2)
    k4 = g(q + dt * k3, t + dt)

    return q + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

def g(q: np.ndarray, t: int) -> np.ndarray: # g(q, t)
    g = np.zeros(18)

    g[0] = 0 # ax = 0
    g[1] = 0 # ay = 0
    g[2] = -9.8 # az = -9.8
    g[3] = q[0] # vx = q[0]
    g[4] = q[1] # vy = q[1]
    g[5] = q[2] # vz = q[2]
    g[6] = 0 # @x = 0
    g[7] = 0 # @y = 0
    g[8] = 0 # @z = 0
    g[9] = q[7] * q[15] - q[8] * q[12] # Rxx
    g[10] = q[7] * q[16] - q[8] * q[13] # Rxy
    g[11] = q[7] * q[17] - q[8] * q[14] # Rxz
    g[12] = q[8] * q[9] - q[6] * q[15] # Ryx
    g[13] = q[8] * q[10] - q[6] * q[16] # Ryy
    g[14] = q[8] * q[11] - q[6] * q[17] # Ryz
    g[15] = q[6] * q[12] - q[7] * q[9] # Rzx
    g[16] = q[6] * q[13] - q[7] * q[10] # Rzy
    g[17] = q[6] * q[14] - q[7] * q[11] # Rzz

    return g