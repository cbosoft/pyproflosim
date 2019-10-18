from matplotlib import pyplot as plt
import networkx as nx

#from pfs.process import Process


def draw(graph, outname=None):
    
    plt.figure()
    nx.draw_networkx(
        graph,
        pos=nx.drawing.spectral_layout(graph),
    )
    plt.draw()
    
    if outname: plt.savefig(outname)
    else: plt.show()
