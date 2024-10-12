import numpy as np
from typing import Tuple
from constantes import Rb, ht, Lt, lt, hf, lf

def SolutionExacte(option: int, rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> Tuple[int, np.ndarray, float, float, float, float]:
    assert option == 1, 'Option invalide, la solution exacte supporte seulement l\'option 1 (force gravitationnelle)'

    cote_oppose = rbi[0] == Lt
    abi = np.array([0, 0, -9.81])
    t_table = temps_de_vol(0.5*abi[2], vbi[2], rbi[2] - ht - Rb)
    t_filet = temps_de_vol(0.5*abi[0], vbi[0], rbi[0] - Lt/2 + (Rb if not cote_oppose else -Rb))
    t_sol = temps_de_vol(0.5*abi[2], vbi[2], rbi[2] - Rb)

    # touche le filet
    yf = rbi[1] + vbi[1]*t_filet
    zf = rbi[2] + vbi[2]*t_filet + 0.5*abi[2]*t_filet**2

    if t_filet < t_table and (-Rb - lf) < yf < (lf + Rb) and (-Rb - hf) < zf < (hf + Rb):
        coup = 2
        vbf = np.array([vbi[0], vbi[1], vbi[2] + abi[2]*t_filet])
        tf = t_filet
        xf = rbi[0] + vbi[0]*t_filet

        return coup, vbf, tf, xf, yf, zf

    # tombe sur la table
    xf = rbi[0] + vbi[0]*t_table
    yf = rbi[1] + vbi[1]*t_table

    if 0 <= yf <= lt and 0 <= xf <= Lt:
        coup = 0 if (xf > Lt/2) ^ cote_oppose else 1
        vbf = np.array([vbi[0], vbi[1], vbi[2] + abi[2]*t_table])
        tf = t_table
        zf = ht + Rb

        return coup, vbf, tf, xf, yf, zf

    # tombe sur le sol
    coup = 3
    vbf = np.array([vbi[0], vbi[1], vbi[2] + abi[2]*t_sol])
    tf = t_sol
    xf = rbi[0] + vbi[0]*t_sol
    yf = rbi[1] + vbi[1]*t_sol
    zf = Rb

    return coup, vbf, tf, xf, yf, zf

def temps_de_vol(a: float, b: float, c: float) -> float:
    if a == 0:
        return -c / b

    delta = b**2 - 4*a*c

    if delta < 0:
        return float('inf')

    t1 = (-b - np.sqrt(delta)) / (2*a)
    t2 = (-b + np.sqrt(delta)) / (2*a)

    return max(t1, t2)

if __name__ == '__main__':
    rbi1 = np.array([0.00, 0.50, 1.10])
    vbi1 = np.array([4.00, 0.00, 0.80])
    wbi1 = np.array([0.00, -70.00, 0.00])

    coup, vbf, tf, xf, yf, zf = SolutionExacte(1, rbi1, vbi1, wbi1)

    print(f'coup: {coup}')
    print(f'vbf: {vbf}')
    print(f'tf: {tf}')
    print(f'xf: {xf}')
    print(f'yf: {yf}')
    print(f'zf: {zf}')