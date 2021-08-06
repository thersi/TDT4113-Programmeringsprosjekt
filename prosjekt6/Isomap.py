""" Modul for Isomap """
import numpy as np
import scipy
from sklearn.utils.graph_shortest_path import graph_shortest_path

class Isomap:
    """ Ismoap-klassen """

    def __init__(self, data,k ):
        """ lager en instans av klassen"""
        self.k=k
        self.data=data

    def distance(self, mat):
        """ beregner avstanden """
        a_value= np.sum(mat**2, axis=1)[:, np.newaxis] #kolonnevektor
        b_value= np.sum(mat**2, axis=1)
        c_value= -2* (mat @ mat.T)
        dist = a_value+b_value+c_value
        dist[dist<0]=0 #Noen verdier blir negative, dette må vi bli kvitt
        #Sjekker om alle verdiene i dist er mindre enn null, lager en boolsk matrise basert på dette
        #bruker det til å indeksere dist, slik bare disse verdiene blir satt til 0
        return dist

    def k_closest(self, mat, k):
        """ Finner de k næmrmeste """
        dist= self.distance(mat)
        dist=np.sqrt(dist)
        index= np.argsort(dist,1)
        for x_var, rad in enumerate(index):
            for kol in rad[k:]:
            # ^hopper over de k første siden de er de nærmeste #Kol fra index matrisa
                dist[x_var, kol]=0 #x= kolonnenr
        return dist

    def calculations(self):
        """ gjør sammensetningen av beregningene med egne data """
        n_var = self.data.shape[0]#how many rows
        shortest_path= graph_shortest_path(self.k_closest(self.data, self.k), False, 'D')
        squared= np.square(shortest_path)
        j_var= np.identity(n_var) - (1/n_var)*np.ones((n_var,n_var))
        b_var = -0.5*(j_var@(squared@j_var))
        #identity takes in a number, how large n row and n
        e_values, e_vectors= scipy.sparse.linalg.eigsh(b_var, k=2, which="LM")
        #Må flippe siden returneres i synkende rekkefølge
        e_values=np.flip(e_values)
        e_vectors=np.flip(e_vectors, axis=1) #flipper over y
        diagonal_matrix= np.diag(e_values) #Lager diagonal matrise
        return e_vectors@scipy.linalg.sqrtm(diagonal_matrix)
