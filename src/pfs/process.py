import copy

import pubchempy
from sympy import Symbol
from sympy import symbols as Symbols
from sympy import solve
from networkx import MultiDiGraph as Graph
import numpy as np

from pfs.colours import C_CMD, C_OKY, C_USR, C_WNG, C_SCS, C_ALT, C_ERR, C_SPL, C_RST
from pfs.stream import Stream, SubStream


class Process(object):
                    

    def __init__(self):
        self.chemicals = dict()
        self.graph     = Graph()
        

    def add_chemical(self, name):
        self.chemicals[name] = chemical_component(name, "name")
        return
        

    def add_node(self, n_type):
        idx = len(self.graph)
        self.graph.add_node(ProcessNode(idx, n_type))
        return
    

    def add_stream(self, name, from_node, into_node, sub_streams=list()):
        self.graph.add_edge(from_node, into_node, stream=stream(name, from_node, into_node, sub_streams))
        return
        

    # def populate_streams(self):
    #     for i in enumerate(self.streams):
    #         self.streams[i].sub_streams = list()
    #         for j, chemical_name in enumerate(self.chemicals):
    #             self.streams[i].sub_streams.append(sub_stream(chemical_name, Symbols(f"Mdot_{chemical_name}_s{self.streams[i].name}") ) )
    #     return

    
    def get_node_streams(self, node):
        inputs = [s for s in self.streams if s.into_node == node]
        outputs = [s for s in self.streams if s.from_node == node]
        return inputs, outputs
    
    
    def nodal_mass_balance(self, node, component="ALL"):

        if type(node) != ProcessNode: node = self.nodes[node]

        in_strms, out_strms = self.get_node_streams(node)

        # get total inlet mass flow
        inlet_flow = 0
        for s in in_strms:
            if component == "ALL":
                inlet_flow += s.get_flow_rate()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        inlet_flow += ss.flow_kgs
        
        # get total outlet mass flow
        outlet_flow = 0
        for s in out_strms:
            if component == "ALL":
                outlet_flow += s.get_flow_rate()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        outlet_flow += ss.flow_kgs
        
        # compare
        discrepency = Symbol('D')
        overall_expression = inlet_flow - outlet_flow + discrepency
        overall_solution = solve(overall_expression, discrepency)
        return overall_expression, overall_solution, inlet_flow, outlet_flow

    
    def overall_mass_balance(self, component="ALL"):

        # get total inlet mass flow
        inlet_flow = 0
        for s in self.streams:
            if s.from_node.type == "input":
                if component == "ALL":
                    inlet_flow += s.get_flow_rate()
                else:
                    for ss in s.sub_streams:
                        if ss.component.lower() == component.lower():
                            inlet_flow += ss.flow_kgs
        
        # get total outlet mass flow
        outlet_flow = 0
        for s in self.streams:
            for n in s.into_node:
                if n.type == "output":
                    if component == "ALL":
                        outlet_flow += s.get_flow_rate()
                    else:
                        for ss in s.sub_streams:
                            if ss.component.lower() == component.lower():
                                outlet_flow += ss.flow_kgs
        
        # compare
        discrepency = Symbol('D')
        overall_expression = inlet_flow - outlet_flow + discprepency
        overall_solution = solve(overall_expression, discrepency)
        return overall_expression, overall_solution, inlet_flow, outlet_flow

    
    def print_stream_table(self, filep=None):
        rows = list()
        rows.append("Compound")
        for i in range(len(self.streams)):
            rows[len(rows) - 1] += ",{}".format(self.streams[i].name)
        for i in range(len(self.chemicals.keys())):
            rows.append(self.chemicals.keys()[i])
            for s in self.streams:
                rows[len(rows) - 1] += ",{}".format(s.sub_streams[i].flow_kgs)
        if filep:
            with open(filep, "w") as csvf:
                for r in rows:
                    csvf.write(r + "\n")
        for r in rows:
            cols = r.split(",")
            row = ""
            for c in cols:
                row += "\t\t  {}".format(c)
            print(row)

    def __repr__(self):
        s = ""
        for g in self.graph:
            s += str(g) + '\n'
        return s


class ProcessNode(object):
    
    def __init__(self, idx, n_type, reactions=list(), conversions=list()):
        self.idx         = idx
        self.n_type      = n_type
        self.reactions   = reactions
        self.conversions = conversions

    def __repr__(self):
        return f'Node {self.idx}'
