from matplotlib import pyplot as plt
import networkx as nx

from pfs.process import Process


def draw(process, outname=None, path=None):

    if path:
        nodes = path

        edges = list()
        for i, (pnode, node) in enumerate(zip(nodes[:-1], nodes[1:])):
            edges.extend([edge for edge in process.graph.edges if edge[0] == pnode and edge[1] == node])
    else:
        nodes = process.graph.nodes
        edges = process.graph.edges
    
    plt.figure()
    nx.draw_networkx(
        process.graph,
        pos=nx.drawing.spectral_layout(process.graph),
        nodelist=nodes,
        edgelist=edges
    )
    plt.draw()

    if path: title = "Process path diagram"
    else: title = "Process diagram"
    plt.title(title)

    
    if outname: plt.savefig(outname)
    else: plt.show()
