import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

'''
 - node labels are keys to the object dict
 - edges connect nodes (representing flow of *information*)
 '''

objdict = dict()


class GenericMISO:

    def __init__(self, name, inputs, output):
        self.name = name
        self.inputs = inputs
        self.output = output

    def add_to_graph(self, G):

        if self.output not in G:
            G.add_node(self.output)
        for i in self.inputs:
            if i not in G:
                G.add_node(i)
            G.add_edge(i, self.output)

    def TF(self):
        raise NotImplementedError('Not implemented; use sub-class')

class Mux(GenericMISO):

    def TF(self):
        global objdict
        return np.sum([objdict[i].TF() for i in self.inputs])

class GeneroSIMO:
    pass


G = nx.MultiDiGraph()

mux = Mux('frank', [f'V00{i}' for i in range(3)], 'T001')
mux.add_to_graph(G)

nx.draw_networkx(G)
plt.show()
