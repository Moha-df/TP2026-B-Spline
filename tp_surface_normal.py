"""TP - Surface B-spline : méthode normale (produit tensoriel).

S(u, v) = sum_i sum_j N_i,p(u) * M_j,q(v) * P_ij

- u fait le tour du contour   : B-spline cubique PÉRIODIQUE (surface fermée, sans couture)
- v va du bas vers le haut     : B-spline cubique "clamped" (passe par le 1er et le dernier étage)
- P_ij : grille de points de contrôle = le contour du fichier empilé sur plusieurs étages.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

# ------------------------------------------------------- grille de contrôle
data = np.loadtxt("points_contour_piece_bspline.csv", delimiter=",", skiprows=1)
contour = data[:, 1:3]                       # (80, 2)
centre = contour.mean(axis=0)

hauteurs = np.array([0, 10, 20, 30, 40], dtype=float)
tailles = np.array([0.5, 1.0, 1.0, 1.0, 0.5])

# P[j, i] = point de contrôle i (autour) de l'étage j (hauteur) -> (5, 80, 3)
P = np.empty((len(hauteurs), len(contour), 3))
for j, (z, s) in enumerate(zip(hauteurs, tailles)):
    P[j, :, :2] = centre + s * (contour - centre)
    P[j, :, 2] = z


# ------------------------------------------------------- fonctions de base
def base_periodique(n, p, u):
    """Matrice (len(u), n) des fonctions de base B-spline périodiques de degré p.
    Noeuds uniformes ; les p dernières fonctions sont repliées sur les p premières."""
    t = np.arange(-p, n + p + 1, dtype=float)
    B = BSpline.design_matrix(u, t, p).toarray()      # (len(u), n + p)
    B[:, :p] += B[:, n:]
    return B[:, :n]


def base_clamped(n, q, v):
    """Matrice (len(v), n) des fonctions de base B-spline clamped de degré q sur [0, 1]."""
    inner = np.linspace(0, 1, n - q + 1)[1:-1]
    t = np.r_[[0.0] * (q + 1), inner, [1.0] * (q + 1)]
    return BSpline.design_matrix(v, t, q).toarray()


def surface(P, p=3, q=3, nu=300, nv=60):
    nv_ctrl, nu_ctrl, _ = P.shape
    u = np.linspace(0, nu_ctrl, nu, endpoint=False)   # un tour complet
    v = np.linspace(0, 1, nv)
    Bu = base_periodique(nu_ctrl, p, u)               # (nu, 80)
    Bv = base_clamped(nv_ctrl, q, v)                  # (nv, 5)
    # S[a, b] = sum_j sum_i Bv[a, j] Bu[b, i] P[j, i]
    S = np.einsum("aj,bi,jic->abc", Bv, Bu, P)
    return np.concatenate([S, S[:, :1]], axis=1)      # on referme pour le dessin


def dessiner(ax, S, P=None, titre=""):
    ax.plot_surface(S[..., 0], S[..., 1], S[..., 2], cmap="viridis",
                    rstride=2, cstride=4, linewidth=0, antialiased=True, alpha=0.9)
    if P is not None:   # réseau de contrôle
        Pf = np.concatenate([P, P[:, :1]], axis=1)
        for etage in Pf:
            ax.plot(*etage.T, "r-", lw=0.5)
        for col in Pf.transpose(1, 0, 2)[::4]:
            ax.plot(*col.T, "r-", lw=0.5)
    ax.set_title(titre)
    ax.view_init(30, -60)


# ------------------------------------------------------- figure
S = surface(P)

P2 = P.copy()
P2[2, 28] += [0, -30, 0]          # on tire vers l'avant un point de contrôle de l'étage du milieu
S2 = surface(P2)

fig = plt.figure(figsize=(16, 5.5))
dessiner(fig.add_subplot(1, 3, 1, projection="3d"), S, P, "points de contrôle (rouge)")
dessiner(fig.add_subplot(1, 3, 2, projection="3d"), S, None, "surface B-spline bicubique")
# coupe à mi-hauteur (v = 0.5) pour bien voir l'effet du point déplacé
ax = fig.add_subplot(1, 3, 3)
m = S.shape[0] // 2
ax.plot(S[m, :, 0], S[m, :, 1], "b-", label="coupe avant")
ax.plot(S2[m, :, 0], S2[m, :, 1], "g-", label="coupe après")
ax.plot(P2[2, :, 0], P2[2, :, 1], "r.", ms=3, label="points de contrôle (étage du milieu)")
ax.plot(*np.array([P[2, 28, :2], P2[2, 28, :2]]).T, "r-o", ms=5)
ax.set_aspect("equal"); ax.legend(fontsize=7, loc="upper right")
ax.set_title("un point de contrôle déplacé (coupe à z = 20)")
plt.tight_layout()
plt.savefig("fig6_surface_bspline.png", dpi=110)
plt.close()

# vérification : la B-spline reste dans l'enveloppe des points de contrôle
print("surface :", S.shape[0], "x", S.shape[1], "points calculés")
print("bas de la surface  z =", S[0, :, 2].min(), "(= 1er étage)")
print("haut de la surface z =", S[-1, :, 2].max(), "(= dernier étage)")
