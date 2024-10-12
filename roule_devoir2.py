import numpy as np
from devoir2 import Devoir2

def RouleDevoir2(simulation_name: str, rbi: np.ndarray, vbi: np.ndarray, wbi: np.ndarray) -> None:
    print('-' * 50 + simulation_name + '-' * 50 + '\n')

    options = [1, 2, 3]
    for option in options:
        coup, vbf, ti, x, y, z = Devoir2(option, rbi, vbi, wbi)

        print(f"option {option}:")
        print(f"coup: {coup}")
        print(f"vbf: {vbf}")
        print(f"ti: {ti[::-50][::-1]}")
        print(f"x: {x[::-50][::-1]}")
        print(f"y: {y[::-50][::-1]}")
        print(f"z: {z[::-50][::-1]}")
        print("\n")