import matplotlib.pyplot as plt
import networkx as nx

from data import components
from colours import col
from process import Process, ProcessNode, NodeType, UnitType
from vis import draw
from chemical_component import ChemicalComponent


def main():
    G = nx.DiGraph()

    G.add_edge(0,1,
               data={
                   'flowrate_kgs':10.0
               }
    )
    G.add_edge(1,2)
    G.add_edge(3,4,
               data={
                   'flowrate_kgs':10.0
               }
    )
    G.add_edge(4,2)
    G.add_edge(2,5)

    draw(G, "test.pdf")
    
    #question: what is mass flow of ethanol through edge 4?

    attrs = nx.get_edge_attributes(G, 'data')

    dfs = list(nx.edge_dfs(G))

    starts = list()
    ends = list()
    
    mixers = list()
    splitters = list()
    
    for prv, ths, nxt in zip(dfs[:-2], dfs[1:-1], dfs[2:]):
        if ths[0] != prv[1]:
            starts.append(ths)
        if ths[1] != nxt[0]:
            ends.append(ths)

    print(G)

    
    for edge, next_edge in zip(dfs[:-1], dfs[1:]):
        
        if next_edge[0] != edge[1]:
            ends.append(edge)
            continue
        if edge not in attrs: continue
        
        print(attrs)

        next_attrs = {'data':{'flowrate_kgs':0}} if not next_edge in attrs else attrs[next_edge]
        #next_attrs['data']['flowrate_kgs'] += attrs[edge]['flowrate_kgs']
            
        nx.set_edge_attributes(G, {next_edge: next_attrs})
        
        attrs = nx.get_edge_attributes(G, 'data')
            
