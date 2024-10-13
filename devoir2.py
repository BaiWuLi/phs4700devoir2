import numpy as np
from typing import Tuple, Callable
from constantes import coup, vbf, ti, x, y, z, mb, Rb, Ab, ht, Lt, lt, hf, lf, df, p, Cv, CM

def Devoir2(option: int, rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> Tuple[coup, vbf, ti, x, y, z]:
    assert option in [1, 2, 3], "Option doit être 1, 2 ou 3"
    assert np.linalg.norm(vbi) <= 35, "La vitesse initiale du centre de masse de la balle ne peut jamais excéder 35 m/s"
    assert np.linalg.norm(wbi) <= 940, "La vitesse angulaire de la balle autour de son centre de masse ne peut excéder 940 rad/s"

    q0 = qi(rbi, vbi, wbi)
    q1 = q0
    coup = -1
    ti = np.array([0])
    x = np.array([rbi[0]])
    y = np.array([rbi[1]])
    z = np.array([rbi[2]])

    t = 0
    dt = 0.0001 # delta t

    while coup == -1:
        q0 = q1
        t += dt
        q1 = RungeKutta4(q0, t, dt, g, option)
        coup = Coup(q0, q1)
        ti = np.append(ti, t)
        x = np.append(x, q1[3])
        y = np.append(y, q1[4])
        z = np.append(z, q1[5])

        if coup == -1:
            continue

        erreur0, erreur1 = erreurs(q0, q1, coup)
        epsilon = 1e-6

        if erreur0 < epsilon:
            q1 = q0
            break
        elif erreur1 < epsilon:
            break

        q1 = q0
        t -= dt
        dt /= 10
        coup = -1

    vbf = q1[0:3]
    ti = compresser_tableau(ti)
    x = compresser_tableau(x)
    y = compresser_tableau(y)
    z = compresser_tableau(z)

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

def RungeKutta4(q: np.ndarray, t: int, dt: int, g: Callable, option: int) -> np.ndarray:
    k1 = g(q, t, option)
    k2 = g(q + dt/2 * k1, t + dt/2, option)
    k3 = g(q + dt/2 * k2, t + dt/2, option)
    k4 = g(q + dt * k3, t + dt, option)

    return q + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

def g(q: np.ndarray, t: int, option: int) -> np.ndarray: # g(q, t)
    Fg = mb * np.array([0, 0, -9.8]) # Force gravitationnelle
    Fv = np.zeros(3) # Force de frottement visqueux
    Fm = np.zeros(3) # Force de Magnus

    if option >= 2:
        Fv = -0.5 * p * Cv * Ab * np.linalg.norm(q[0:3]) * q[0:3]
    if option == 3:
        Fm = 4 * np.pi * Rb**3 * p * CM * np.cross(q[6:9], q[0:3])

    F = Fg + Fv + Fm

    g = np.zeros(18)

    g[0] = F[0] / mb # ax
    g[1] = F[1] / mb # ay
    g[2] = F[2] / mb # az
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

def Coup(q0, q1):
    x0, x1 = q0[3], q1[3]  # positions x (précédente et actuelle)
    y1 = q1[4]             # position y actuelle
    z0, z1 = q0[5], q1[5]  # positions z (précédente et actuelle)

    # Vérification de la collision avec le filet
    traverse_plan_filet = (x0 < (Lt/2 - Rb) <= x1) or (x1 <= Lt/2 + Rb < x0) # traverse par la gauche ou par la droite
    dans_zone_filet = ((-df - Rb) < y1 < (lt + df + Rb)) and ((ht + Rb) <= z1 < (ht + hf + Rb))
    if traverse_plan_filet and dans_zone_filet:
        return 2

    # Vérification de la collision avec la table
    traverse_plan_table = z0 > ht + Rb >= z1
    dans_zone_table = (0 <= x1 <= Lt) and (0 <= y1 <= lt)
    if traverse_plan_table and dans_zone_table:
        if (x1 > Lt/2) ^ (x1 < x0):
            return 0
        else:
            return 1

    # Vérification de la collision avec le sol
    traverse_plan_sol = z0 > 0 + Rb >= z1
    if traverse_plan_sol:
        return 3

    return -1  # La balle ne touche rien

def erreurs(q0: np.ndarray, q1: np.ndarray, coup: int) -> Tuple[float, float]:
    erreur0 = abs((ht + Rb) - q0[5])
    erreur1 = abs((ht + Rb) - q1[5])
    if coup == 2 and q1[3] < Lt/2:
        erreur0 = abs((Lt/2 - Rb) - q0[3])
        erreur1 = abs((Lt/2 - Rb) - q1[3])
    if coup == 2 and q1[3] >= Lt/2:
        erreur0 = abs((Lt/2 + Rb) - q0[3])
        erreur1 = abs((Lt/2 + Rb) - q1[3])
    if coup == 3:
        erreur0 = abs(Rb - q0[5])
        erreur1 = abs(Rb - q1[5])
    return erreur0, erreur1

def compresser_tableau(arr: np.ndarray, taille_max=500) -> np.ndarray:
    if len(arr) <= taille_max:
        return arr

    interval = int(np.ceil((len(arr) - 2) / taille_max))
    return np.concatenate((arr[:1], arr[interval:-1:interval], arr[-1:]))