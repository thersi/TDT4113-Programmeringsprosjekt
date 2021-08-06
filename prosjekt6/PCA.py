import numpy as np
import scipy
from scipy.sparse.linalg import eigs
from numpy.linalg import eigh



class PCA():
    def __init__(self, data):
        assert data.shape[1] >= 2 #Her sjekker vi om dim>=2
        self.data = data


    def fitTransform(self):
        center_value= self.center()
        cov_matrix = np.cov(center_value, rowvar=False)  # satisfies part b) #Rovar fordi vi har
        #Store D er dim for selve datatset
        #Lille d er hva du reduserer til, er alltid to i dette tilfellet

        if center_value.shape[1]>3:
            _, e_vector= scipy.sparse.linalg.eigs(cov_matrix, k=2) #K finner hvor mange egenvektorer siden vi skal bare ha 2, kommer i sortert rekkefølge
            return (e_vector.T @ center_value.T).T
        _, e_vector=np.linalg.eigh(cov_matrix)
        return (e_vector[:, -2:].T @ center_value.T).T


    def center(self):
        my = self.data.mean(axis=0)  # Finner gjennomsnittet av den kolonnen
        my_matrix = np.ones(self.data.shape)  # FInenr da en vedå bruke shape
        my_matrix *= my
        return self.data - my_matrix


if __name__ == '__main__':
    swiss=np.genfromtxt("swiss_data2.csv", delimiter=",")
    pca=PCA(swiss)
    print(pca.fitTransform())
