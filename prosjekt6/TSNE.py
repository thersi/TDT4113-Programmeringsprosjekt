""" Modul for TSNE """
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE as T_SNE
from timer import Timer


class TSNE:
    """ TSNE - klassen """
    def __init__(self):
        self.iterations = 300
        self.e_var = 500
        self.a_var = 0.8
        self.k_var = 30
        self.x_var, self.x_label = get_data()

    def get_data(self):
        """
        Laster verdiene fra csv-filen.
        Utløser FileNotFound ved problem.

        """
        try:
            self.x_var, self.x_label = np.genfromtxt("digits.csv", delimiter=","), \
                                       np.genfromtxt("digits_label.csv",
                                        delimiter=",")
        except Exception:
            raise Exception("File not found or wrong I/O")

    def calculate_result(self):
        """ Kalukluerer reusltatet fra data og printer """
        print("Starting t-SNE...")

        self.x_var = self.x_var[:3000, :]
        self.x_label = self.x_label[:3000]

        t_var = Timer("setup")

        n_features = self.x_var.shape[0]
        euc_dis = pairwise_distances(self.x_var)
        k_nn = k_nearest(euc_dis, self.k_var)

        p_var = get_pairwise(euc_dis.shape, k_nn)

        del k_nn
        del euc_dis

        y_var = np.random.randn(n_features, 2) * 1e-4
        gain = np.full((n_features, 2), 1.0)
        delta = np.full((n_features, 2), 0.0)

        t_var.stop()

        t_var = Timer("t-SNE")

        for n_var in range(self.iterations):
            a_var = 0.5 if n_var < 250 else self.a_var

            if n_var % 10 == 0:
                print(f"Iteration {n_var}: a_var = {a_var},"
                      f" p_var scaling factor = {1 if n_var > 100 else 4}")

            q_var = 1 / (1 + squared_distances(y_var))

            q_var[range(n_features), range(n_features)] = 0
            q_great_var = q_var / np.sum(q_var)

            t_var = Timer("grad")

            g_var = (p_var - q_great_var) * q_var if n_var > 100 else \
                (4 * p_var - q_great_var) * q_var
            s_var = np.diag(np.sum(g_var, axis=1))
            grad = 4 * (s_var - g_var) @ y_var
            t_var.stop()

            gain[np.sign(grad) == np.sign(delta)] *= 0.8
            gain[np.sign(grad) != np.sign(delta)] += 0.2
            gain[gain < 0.01] = 0.01

            delta = (a_var * delta) - (self.e_var * gain * grad)
            y_var += delta

        diff = t_var.stop()
        print(f"Average time per iteration: {diff / self.iterations / 1e9:.2f}s")
        self.plot(y_var)

    def plot(self, y_var):
        """ Plotter dataen """
        plt.jet()
        plt.scatter(y_var[:, 0], y_var[:, 1], s=10, c=self.x_label)
        plt.show()


def get_data():
    """
       Laster verdiene fra csv-filen.
       Utløser FileNotFound ved problem.
       """

    try:
        return np.genfromtxt("digits.csv", delimiter=","), np.genfromtxt("digits_label.csv",
                                                                         delimiter=",")
    except Exception:
        raise Exception("An error occurred")

def calculate_distances(x_var):
    """
    Regner ut eukledisk distanse mellom punkter
        """

    x_sqr = x_var * x_var

    v_var = np.sum(x_sqr, axis=1, keepdims=True)

    xxt = np.matmul(x_var, x_var.T)
    euc_dis = v_var.T + v_var - 2 * xxt

    return np.sqrt(np.abs(euc_dis))


def k_nearest(euc_dis, k_var):
    """
    Finne de k-nærmeste naboene innenfor avstandsatrisen (euklidiske)
    der edm må være en m*m matrise
    """
    k_nn = np.copy(euc_dis)
    for row in k_nn:
        k_smallest = np.argpartition(row, k_var + 1)[k_var + 1:]
        row[k_smallest] = 0

    return k_nn


def get_pairwise(shape, k_nn):
    """
    beregner parvis likhet fra resultatet i k_nn-grafen
    """
    p_var = ((k_nn + k_nn.T > 0).astype(float))
    return p_var / np.sum(p_var)


def pairwise_distances(x_var):
    """
    Kalkulerer den euclidiske avstanden mellom punkter i en n-dimensjonal tabell,
    bruker medtoden for kvadrert euklidisk avstand
    returnerer en matrise bestående av de parvise euklidiske avstandene
    """

    v_var = np.sum(x_var * x_var, axis=1, keepdims=True)
    return np.sqrt(np.abs(v_var.T + v_var - 2 * (x_var @ x_var.T)))


def squared_distances(x_var):
    """
    kvadrerer de euklidiske avstandene matrix of pairwise squared euclidean distances
    """
    v_var = np.sum(x_var * x_var, axis=1, keepdims=True)
    return v_var.T + v_var - 2 * (x_var @ x_var.T)
