"""TP - Reconstruction d'un contour : méthode "points milieux".

Entre le point 1 et 2 on met un point au milieu, entre 2 et 3 aussi, etc.,
puis on relie les points milieux entre eux. On peut recommencer.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = np.loadtxt("points_contour_piece_bspline.csv", delimiter=",", skiprows=1)
pts = data[:, 1:3]


def milieux(P):
    """Milieu de chaque couple de points consécutifs (contour fermé => on boucle)."""
    return (P + np.roll(P, -1, axis=0)) / 2


fig, axs = plt.subplots(1, 3, figsize=(15, 5))
P = pts.copy()
for ax, it in zip(axs, [1, 2, 3]):
    M = milieux(P)
    ax.plot(*np.vstack([P, P[0]]).T, "k.-", lw=0.4, label="points de départ")
    ax.plot(*np.vstack([M, M[0]]).T, "m-o", ms=3, label="milieux reliés")
    ax.set_title(f"itération {it}"); ax.axis("equal"); ax.legend(fontsize=7)
    P = M
plt.tight_layout(); plt.savefig("fig4_methode_milieux.png", dpi=120); plt.close()
