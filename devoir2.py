import numpy as np
from typing import Tuple, Callable
from constantes import Rb, ht, Lt, lt, hf, lf, coup, vbf, ti, x, y, z

def Devoir2(option: int, rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> Tuple[coup, vbf, ti, x, y, z]:
    t = 0 # t0
    dt = 0.001 # delta t

    q0 = qi(rbi, vbi, wbi)
    q1 = RungeKutta4(q0, t, dt, g)
    t += dt
    coup = Coup(q0, q1)
    ti = np.array([t])
    x = np.array([q1[3]])
    y = np.array([q1[4]])
    z = np.array([q1[5]])

    while coup == -1:
        q0 = q1
        q1 = RungeKutta4(q0, t, dt, g)
        t += dt
        coup = Coup(q0, q1)
        ti = np.append(ti, t)
        x = np.append(x, q1[3])
        y = np.append(y, q1[4])
        z = np.append(z, q1[5])

        if coup == -1:
            continue

        epsilon = 1e-6

        if coup == 0 or coup == 1:
            erreur0 = abs((ht + Rb) - q0[5])
            erreur1 = abs((ht + Rb) - q1[5])
        if coup == 2:
            erreur0 = abs((lt/2 - Rb) - q0[3])
            erreur1 = abs((lt/2 - Rb) - q1[3])
        if coup == 3:
            erreur0 = abs(Rb - q0[5])
            erreur1 = abs(Rb - q1[5])

        if erreur0 < epsilon:
            q1 = q0
            break
        elif erreur1 < epsilon:
            break

        q1 = q0
        t -= dt
        dt /= 10
        t += dt
        coup = -1



    vbf = np.array([q1[0], q1[1], q1[2]])
    return coup, vbf, ti, x, y, z


def qi(rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> np.ndarray:
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

def Coup(q0, q1):
    x0, x1 = q0[3], q1[3]  # positions x (précédente et actuelle)
    y1 = q1[4]             # position y actuelle
    z0, z1 = q0[5], q1[5]  # positions z (précédente et actuelle)

    # Vérification de la collision avec le filet
    traverse_plan_filet = (x0 < (lt/2 - Rb) <= x1) or (x1 <= lt/2 + Rb < x0) # traverse par la gauche ou par la droite
    dans_zone_filet = ((-lf/2 - Rb) < y1 < (lf/2 + Rb)) and ((ht + Rb) <= z1 < (ht + hf + Rb))
    if traverse_plan_filet and dans_zone_filet:
        return 2

    # Vérification de la collision avec la table
    traverse_plan_table = z0 > ht + Rb >= z1
    dans_zone_table = (0 <= x1 <= Lt) and (0 <= y1 <= lt)
    if traverse_plan_table and dans_zone_table:
        return 0 if DansZoneAdversaire(x0, x1) else 1

    # Vérification de la collision avec le sol
    traverse_plan_sol = z0 > 0 + Rb >= z1
    if traverse_plan_sol:
        return 3

    return -1  # La balle ne touche rien

def DansZoneAdversaire(x0, x1):
    # Cote de la table = droite si (x1 > Lt/2), gauche sinon
    # Direction de la balle = vers la gauche si (x1 < x0), vers la droite sinon
    # Table de verité
    # (x1 > Lt/2) | (x1 < x0) | DansZoneAdversaire
    #     0       |     0     |        0
    #     0       |     1     |        1
    #     1       |     0     |        1
    #     1       |     1     |        0
    # Donc, DansZoneAdversaire = (x1 > Lt/2) XOR (x1 < x0)
    return (x1 > Lt/2) ^ (x1 < x0)

def RungeKutta4(q: np.ndarray, t: int, dt: int, g: Callable) -> np.ndarray:
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