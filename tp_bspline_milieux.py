# Méthode des points milieux
# Idée : entre le point 1 et le point 2 je mets un point au milieu,
# entre le point 2 et le point 3 aussi, etc.
# Ensuite je relie tous les points du milieu entre eux.
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

# 2) Faire nb fois la méthode du milieu
plt.figure(figsize=(5 * nb, 5))

for essai in range(1, nb + 1):           # essai = 1, 2, ..., nb
    n = len(X)
    Xm = []                              # x des points milieux
    Ym = []                              # y des points milieux

    for i in range(n):
        j = i + 1                        # le point suivant
        if j == n:                       # si on est au dernier point,
            j = 0                        # le suivant c'est le premier (contour fermé)
        Xm.append((X[i] + X[j]) / 2)     # milieu = moyenne des 2 points
        Ym.append((Y[i] + Y[j]) / 2)

    # 3) Dessin : points de départ en noir, milieux reliés en rose
    plt.subplot(1, nb, essai)
    plt.plot(X + [X[0]], Y + [Y[0]], "k.-", linewidth=0.5)     # départ
    plt.plot(Xm + [Xm[0]], Ym + [Ym[0]], "m-o", markersize=3)  # milieux
    plt.title("essai " + str(essai))
    plt.axis("equal")

    # 4) Les milieux deviennent les nouveaux points pour l'essai suivant
    X = Xm
    Y = Ym

plt.savefig("fig4_methode_milieux.png", dpi=120)
print("fini")
