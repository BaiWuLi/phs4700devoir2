import numpy as np
from  roule_devoir2 import RouleDevoir2

if __name__ == '__main__':
    # Coup 1
    rbi1 = np.array([0.00, 0.50, 1.10])
    vbi1 = np.array([4.00, 0.00, 0.80])
    wbi1 = np.array([0.00, -70.00, 0.00])
    RouleDevoir2('Coup 1', rbi1, vbi1, wbi1)

    # Coup 2
    rbi2 = np.array([0.00, 0.40, 1.14])
    vbi2 = np.array([10.00, 1.00, 0.20])
    wbi2 = np.array([0.00, 100.00, -50.00])
    RouleDevoir2('Coup 2', rbi2, vbi2, wbi2)

    # Coup 3
    rbi3 = np.array([2.74, 0.50, 1.14])
    vbi3 = np.array([-5.00, 0.00, 0.20])
    wbi3 = np.array([0.00, 100.00, 0.00])
    RouleDevoir2('Coup 3', rbi3, vbi3, wbi3)

    # Coup 4
    rbi4 = np.array([0.00, 0.30, 1.00])
    vbi4 = np.array([10.00, -2.00, 0.20])
    wbi4 = np.array([0.00, 10.00, -100.00])
    RouleDevoir2('Coup 4', rbi4, vbi4, wbi4)
