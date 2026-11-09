"""TP - Reconstruction d'un contour par B-spline (version la plus simple possible)

Partie 1 : méthode normale (B-spline de degré p, points de contrôle).
Partie 2 : méthode "points milieux" (idée de l'étudiant) :
           entre le point 1 et 2 on met un point au milieu, entre 2 et 3 aussi,
           et on relie les points milieux entre eux.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.interpolate import make_lsq_spline

# ---------------------------------------------------------------- 4. données
data = np.loadtxt("points_contour_piece_bspline.csv", delimiter=",", skiprows=1)
x, y = data[:, 1], data[:, 2]
pts = np.column_stack([x, y])
# contour fermé : on rajoute le 1er point à la fin
pts_closed = np.vstack([pts, pts[0]])

plt.figure(figsize=(5, 5))
plt.plot(x, y, "k.")
plt.axis("equal"); plt.title("Nuage de points du contour")
plt.savefig("fig1_nuage.png", dpi=120); plt.close()

# ------------------------------------------------- 5. B-spline (méthode normale)
# paramètre t = abscisse curviligne normalisée (longueur de corde)
d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts_closed, axis=0), axis=1))]
t = d / d[-1]


def bspline(p, n_ctrl=40):
    """B-spline de degré p avec n_ctrl points de contrôle (moindres carrés)."""
    n_inner = n_ctrl - p - 1                       # noeuds intérieurs
    inner = np.linspace(0, 1, n_inner + 2)[1:-1]
    knots = np.r_[[0] * (p + 1), inner, [1] * (p + 1)]   # vecteur de noeuds "clamped"
    spl = make_lsq_spline(t, pts_closed, knots, k=p)
    return spl, spl.c                               # courbe et points de contrôle


tt = np.linspace(0, 1, 500)
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
for ax, p in zip(axs.ravel(), [1, 2, 3, 4]):
    spl, ctrl = bspline(p)
    c = spl(tt)
    ax.plot(x, y, "k.", label="contour initial")
    ax.plot(ctrl[:, 0], ctrl[:, 1], "r--o", ms=4, lw=0.8, label="points de contrôle")
    ax.plot(c[:, 0], c[:, 1], "b-", label="B-spline")
    err = np.linalg.norm(spl(t) - pts_closed, axis=1)
    ax.set_title(f"degré p={p}  (erreur max = {err.max():.2f})")
    ax.axis("equal")
    ax.legend(fontsize=7)
    print(f"p={p} : erreur moyenne {err.mean():.3f}, max {err.max():.3f}")
plt.tight_layout(); plt.savefig("fig2_bspline_degres.png", dpi=120); plt.close()

# modification d'un point de contrôle (objectif du TP)
spl, ctrl = bspline(3)
ctrl2 = ctrl.copy()
ctrl2[5] += [10, 10]                                # on déplace le point n°5
spl2 = type(spl)(spl.t, ctrl2, spl.k)
plt.figure(figsize=(5, 5))
plt.plot(x, y, "k.", label="contour initial")
plt.plot(*spl(tt).T, "b-", label="avant")
plt.plot(*spl2(tt).T, "g-", label="après")
plt.plot(*ctrl2.T, "r--o", ms=3, lw=0.6)
plt.axis("equal"); plt.legend(); plt.title("Effet d'un point de contrôle déplacé")
plt.savefig("fig3_modif_controle.png", dpi=120); plt.close()

# ------------------------------------------------- Méthode "points milieux"
def milieux(P):
    """Pour chaque couple de points consécutifs (1,2), (2,3), ... :
    on crée le point du milieu. Contour fermé => on boucle."""
    return (P + np.roll(P, -1, axis=0)) / 2


fig, axs = plt.subplots(1, 3, figsize=(15, 5))
P = pts.copy()
for ax, it in zip(axs, [1, 2, 3]):
    M = milieux(P)                                   # points milieux
    ax.plot(*np.vstack([P, P[0]]).T, "k.-", lw=0.4, label="points de départ")
    ax.plot(*np.vstack([M, M[0]]).T, "m-o", ms=3, label="milieux reliés")
    ax.set_title(f"itération {it}"); ax.axis("equal"); ax.legend(fontsize=7)
    P = M                                            # on recommence avec les milieux
plt.tight_layout(); plt.savefig("fig4_methode_milieux.png", dpi=120); plt.close()
