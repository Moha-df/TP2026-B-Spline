# Méthode "couper les coins" (algorithme de Chaikin)
#
# Mon idée de départ : mettre un point au milieu entre 2 points.
# Problème : le milieu est SUR le segment, donc la forme ne change pas.
# Et si on garde seulement les milieux, on a toujours 80 points
# et des angles toujours aussi pointus (juste décalés).
#
# Correction : sur chaque segment [P, Q] on met DEUX points :
#   - un au quart      :  3/4 P + 1/4 Q   (proche de P)
#   - un aux trois quarts : 1/4 P + 3/4 Q (proche de Q)
# et on SAUTE les anciens points P et Q.
# Comme les anciens points étaient les coins, on coupe chaque coin :
# l'angle devient deux angles plus doux. Le nombre de points double à chaque fois.
# En répétant, la courbe devient lisse : c'est une B-spline de degré 2
# dont les points de départ sont les points de contrôle.
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

X0 = list(X)     # on garde les points de départ pour les dessiner
Y0 = list(Y)

# 2) Faire nb fois : couper tous les coins
plt.figure(figsize=(5 * nb, 10))

for essai in range(1, nb + 1):           # essai = 1, 2, ..., nb
    n = len(X)
    Xnew = []
    Ynew = []

    for i in range(n):
        j = i + 1                        # le point suivant
        if j == n:                       # si on est au dernier point,
            j = 0                        # le suivant c'est le premier (contour fermé)

        # point au quart du segment (proche du point i)
        Xnew.append(0.75 * X[i] + 0.25 * X[j])
        Ynew.append(0.75 * Y[i] + 0.25 * Y[j])
        # point aux trois quarts du segment (proche du point j)
        Xnew.append(0.25 * X[i] + 0.75 * X[j])
        Ynew.append(0.25 * Y[i] + 0.75 * Y[j])
        # l'ancien point i n'est PAS remis : c'est lui le coin qu'on coupe

    # 3) Dessin
    # Ligne du haut : toute la forme, avec les points de départ en noir
    plt.subplot(2, nb, essai)
    plt.plot(X0, Y0, "k.", markersize=4)
    plt.plot(Xnew + [Xnew[0]], Ynew + [Ynew[0]], "m-", linewidth=1)
    plt.title("essai " + str(essai) + " : " + str(len(Xnew)) + " points")
    plt.axis("equal")

    # Ligne du bas : ZOOM sur un coin pour voir qu'il est coupé
    plt.subplot(2, nb, nb + essai)
    plt.plot(X + [X[0]], Y + [Y[0]], "k-o", linewidth=0.8, markersize=4,
             label="avant (noir)")
    plt.plot(Xnew + [Xnew[0]], Ynew + [Ynew[0]], "m-o", linewidth=1, markersize=3,
             label="après (rose)")
    plt.legend(loc="lower right", fontsize=7)
    plt.xlim(0, 30)
    plt.ylim(30, 60)
    plt.title("zoom sur un coin")

    # 4) Les nouveaux points servent pour l'essai suivant
    X = Xnew
    Y = Ynew

plt.tight_layout()
plt.savefig("fig4_coins_coupes.png", dpi=120)
print("fini, il y a", len(X), "points à la fin")
