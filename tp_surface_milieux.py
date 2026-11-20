# Surface : ma version simple (on coupe les coins, comme pour la courbe)
#
# Idée : on fabrique une "grille" de points de contrôle en empilant le contour
# à plusieurs hauteurs z (comme des étages). Chaque étage est un peu plus grand
# ou plus petit, ça donne une pièce en 3D.
#
# Ensuite on fait EXACTEMENT comme pour la courbe (Chaikin) :
#   1) sur chaque étage (le contour, fermé) on coupe les coins ;
#   2) sur chaque colonne (de bas en haut, ouverte) on coupe aussi les coins.
# On répète : la grille devient de plus en plus fine et la surface devient lisse.
import sys
import numpy as np            # seulement pour le dessin 3D (plot_surface veut des tableaux)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    nb = int(sys.argv[1])
else:
    nb = 3

# 1) Lire le contour
fichier = open("points_contour_piece_bspline.csv")
lignes = fichier.readlines()
fichier.close()
X = []
Y = []
for i in range(1, len(lignes)):
    morceaux = lignes[i].split(",")
    X.append(float(morceaux[1]))
    Y.append(float(morceaux[2]))

# centre de la forme (moyenne des points) pour agrandir/rétrécir autour
cx = sum(X) / len(X)
cy = sum(Y) / len(Y)

# 2) La grille : un étage = le contour agrandi/rétréci, posé à une hauteur z
hauteurs = [0, 10, 20, 30, 40]
tailles = [0.5, 1.0, 1.0, 1.0, 0.5]       # petit en bas et en haut : bords arrondis

# grille[k][i] = point (x, y, z) numéro i de l'étage k
grille = []
for k in range(len(hauteurs)):
    etage = []
    for i in range(len(X)):
        x = cx + tailles[k] * (X[i] - cx)
        y = cy + tailles[k] * (Y[i] - cy)
        etage.append([x, y, hauteurs[k]])
    grille.append(etage)


def couper_coins(points, ferme):
    """Chaikin sur une liste de points [x, y, z].
    ferme=True : le dernier point est relié au premier (le contour).
    ferme=False : on garde le premier et le dernier point (bas et haut)."""
    n = len(points)
    nouveaux = []
    if not ferme:
        nouveaux.append(points[0])
    if ferme:
        nb_segments = n
    else:
        nb_segments = n - 1
    for i in range(nb_segments):
        j = (i + 1) % n
        P = points[i]
        Q = points[j]
        quart = [0.75 * P[c] + 0.25 * Q[c] for c in range(3)]
        trois_quarts = [0.25 * P[c] + 0.75 * Q[c] for c in range(3)]
        nouveaux.append(quart)
        nouveaux.append(trois_quarts)
    if not ferme:
        nouveaux.append(points[-1])
    return nouveaux


def dessiner(ax, g, titre):
    # on referme le contour pour que la surface fasse le tour
    Xs = [[p[0] for p in etage] + [etage[0][0]] for etage in g]
    Ys = [[p[1] for p in etage] + [etage[0][1]] for etage in g]
    Zs = [[p[2] for p in etage] + [etage[0][2]] for etage in g]
    ax.plot_surface(np.array(Xs), np.array(Ys), np.array(Zs), cmap="viridis", edgecolor="k", linewidth=0.1)
    ax.set_title(titre)
    ax.view_init(30, -60)


fig = plt.figure(figsize=(5 * (nb + 1), 5))
ax = fig.add_subplot(1, nb + 1, 1, projection="3d")
dessiner(ax, grille, "grille de départ : " + str(len(grille)) + " x " + str(len(grille[0])))

for essai in range(1, nb + 1):
    # 1) couper les coins sur chaque étage (sens du contour)
    grille = [couper_coins(etage, True) for etage in grille]
    # 2) couper les coins sur chaque colonne (de bas en haut)
    colonnes = []
    for i in range(len(grille[0])):
        colonne = [grille[k][i] for k in range(len(grille))]
        colonnes.append(couper_coins(colonne, False))
    # on remet sous forme d'étages
    grille = [[colonnes[i][k] for i in range(len(colonnes))] for k in range(len(colonnes[0]))]

    ax = fig.add_subplot(1, nb + 1, essai + 1, projection="3d")
    dessiner(ax, grille, "essai " + str(essai) + " : " + str(len(grille)) + " x " + str(len(grille[0])))

plt.tight_layout()
plt.savefig("fig5_surface_coins_coupes.png", dpi=110)
print("fini, grille de", len(grille), "x", len(grille[0]), "points")
