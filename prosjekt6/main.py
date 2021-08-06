# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt

from Isomap import Isomap
from PCA import PCA
from TSNE import TSNE


def swiss():
    # Use a breakpoint in the code line below to debug your script.
    swiss = np.genfromtxt("swiss_data2.csv", delimiter=",")
    pca = PCA(swiss)
    results = pca.fitTransform()
    clr = [np.sqrt(point[0] ** 2 + point[1] ** 2) for point in results]  # lager en liste fra en loop, rare greier
    plt.scatter(results[:, 0], results[:, 1], s=20, marker=".", c=clr, cmap="jet")  # Henter kol i første og andre
    plt.show()


def digits():
    digit = np.genfromtxt("digits.csv", delimiter=",")
    pca = PCA(digit)
    results = pca.fitTransform()
    digits_label = np.genfromtxt("digits_label.csv", delimiter=",")
    plt.scatter(results[:, 0], results[:, 1], s=20, marker=".", c=digits_label,
                cmap="jet")  # Henter kol i første og andre
    plt.show()


def isoplot_swiss():
    swiss = np.genfromtxt("swiss_data2.csv", delimiter=",")
    iso = Isomap(swiss, 30)
    results = iso.calculations()
    clr = np.arange(results.shape[0])
    plt.scatter(results[:, 0], results[:, 1], s=20, marker=".", c=clr, cmap="jet")  # Henter kol i første og andre
    plt.show()


def isoplot_digits():
    swiss = np.genfromtxt("digits.csv", delimiter=",")
    iso = Isomap(swiss, 30)
    results = iso.calculations()
    clr = np.arange(results.shape[0])
    plt.scatter(results[:, 0], results[:, 1], s=20, marker=".", c=clr, cmap="jet")  # Henter kol i første og andre
    plt.show()


def run_TSNE():
    t_sne = TSNE()
    t_sne.calculate_result()


if __name__ == '__main__':
    run_TSNE()
