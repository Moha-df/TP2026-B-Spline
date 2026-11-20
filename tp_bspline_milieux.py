# Méthode des points milieux (lissage des angles)
# Idée : entre le point 1 et le point 2 je mets un point au milieu,
# entre le point 2 et le point 3 aussi, etc.
# Je ne garde QUE les milieux (je saute les anciens points) : les coins sont coupés
# donc la courbe s'adoucit à chaque itération.
# (Avant je gardais les anciens points en plus : la courbe ne changeait pas du tout.)
import sys
import matplotlib
matplotlib.use("Agg")          # pour enregistrer l'image sans ouvrir de fenêtre
import matplotlib.pyplot as plt

# Nombre d'itérations donné en argument : python tp_bspline_milieux.py 5
# (si on ne donne rien, on prend 3)
if len(sys.argv) > 1:
    nb = int(sys.argv[1])
else:
    nb = 3

# 1) Lire le fichier avec les points
fichier = open("points_contour_piece_bspline.csv")
lignes = fichier.readlines()
fichier.close()

X = []   # liste des x
Y = []   # liste des y
for i in range(1, len(lignes)):          # on saute la 1ère ligne (index,x,y)
    morceaux = lignes[i].split(",")
    X.append(float(morceaux[1]))
    Y.append(float(morceaux[2]))

# 2) Faire nb fois : on AJOUTE un point au milieu entre chaque couple de points
plt.figure(figsize=(5 * nb, 10))

for essai in range(1, nb + 1):           # essai = 1, 2, ..., nb
    n = len(X)
    Xnew = []                            # nouvelle liste de x (points + milieux)
    Ynew = []                            # nouvelle liste de y
    Xm = []                              # seulement les milieux (pour les dessiner en rose)
    Ym = []

    for i in range(n):
        j = i + 1                        # le point suivant
        if j == n:                       # si on est au dernier point,
            j = 0                        # le suivant c'est le premier (contour fermé)
        xm = (X[i] + X[j]) / 2           # milieu = moyenne des 2 points
        ym = (Y[i] + Y[j]) / 2

        Xnew.append(xm)                  # on garde seulement le milieu (l'ancien point saute)
        Ynew.append(ym)
        Xm.append(xm)
        Ym.append(ym)

    # 3) Dessin : points de départ en noir, nouveaux milieux en rose
    # Ligne du haut : toute la forme (juste la ligne, sans les points)
    plt.subplot(2, nb, essai)
    plt.plot(Xnew + [Xnew[0]], Ynew + [Ynew[0]], "k-", linewidth=0.5)  # on relie tout
    plt.title("essai " + str(essai) + " : " + str(len(Xnew)) + " points")
    plt.axis("equal")

    # Ligne du bas : ZOOM sur une petite zone pour bien voir tous les points
    plt.subplot(2, nb, nb + essai)
    plt.plot(X + [X[0]], Y + [Y[0]], "k-", linewidth=0.5)       # ancienne ligne (noir)
    plt.plot(Xnew + [Xnew[0]], Ynew + [Ynew[0]], "m-", linewidth=0.8)  # nouvelle ligne (rose)
    plt.plot(X, Y, "ko", markersize=5, label="anciens points (noir)")
    plt.plot(Xm, Ym, "mo", markersize=3, label="nouveaux milieux (rose)")
    plt.legend(loc="lower right", fontsize=7)
    plt.xlim(10, 30)
    plt.ylim(40, 60)
    plt.title("zoom")

    # 4) La nouvelle liste (points + milieux) sert pour l'essai suivant
    X = Xnew
    Y = Ynew

plt.savefig("fig4_milieux_3_iterations.png", dpi=120)
print("fini, il y a", len(X), "points à la fin")
