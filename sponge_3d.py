import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def genera_spugna_3d(dim=15):
    x, y, z = np.mgrid[-dim:dim+1, -dim:dim+1, -dim:dim+1]
    solido = np.zeros_like(x, dtype=bool)
    
    for i in range(-dim, dim+1):
        for j in range(-dim, dim+1):
            for k in range(-dim, dim+1):
                if i == 0 and j == 0 and k == 0: continue
                if abs(i) == 1 or abs(j) == 1 or abs(k) == 1: continue
                mcd_totale = math.gcd(math.gcd(abs(i), abs(j)), abs(k))
                if mcd_totale > 1:
                    solido[i+dim, j+dim, k+dim] = True
                    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("La Spugna Aritmetica 3D di Enrico", fontsize=16)
    ax.voxels(solido, facecolors='black', edgecolors='gray', alpha=0.6)
    ax.set_xlabel('Asse X')
    ax.set_ylabel('Asse Y')
    ax.set_zlabel('Asse Z')
    print("Usa il mouse per trascinare e ruotare la spugna 3D!")
    plt.show()

if __name__ == "__main__":
    genera_spugna_3d(15)
