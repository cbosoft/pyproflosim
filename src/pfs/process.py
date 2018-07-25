import pubchempy
from sympy import Symbol
from sympy import symbols as Symbols
from sympy import solve
from networkx import MultiDiGraph as Graph
import numpy as np

from pfs.colours import C_CMD, C_OKY, C_USR, C_WNG, C_SCS, C_ALT, C_ERR, C_SPL, C_RST
from pfs.stream import Stream, SubStream
from pfs.chemical_component import ChemicalComponent
from pfs.exception import PFS_Error, PFS_Key_Duplication_Error
from pfs.types import NodeType, UnitType


class Process(object):
                    

    def __init__(self):
        self.chemicals = dict()
        self.graph     = Graph()
        self.nodes     = dict()
        self.streams   = dict()

        
    def __repr__(self):
        nodes = ''.join('\t'+str(n)+'\n' for n in self.graph.nodes())
        streams = ''.join('\t'+str(data['stream'])+'\n' for __, __, data in self.graph.edges.data())
        return f"Process with nodes:\n{nodes}streams:\n{streams}"

    def __next__(self):
        for edge in self.graph.edges():
            yield edge['stream']
        

    def add_chemical(self, name):
        self.chemicals[name] = ChemicalComponent(name)
        return
        

    def add_node(self, name, n_type, u_type):

        if name in self.nodes:
            raise PFS_Key_Duplication_Error("Cannot have multiple nodes with the same name!")
        
        idx = len(self.graph)
        pn = ProcessNode(idx, name, n_type, u_type)
        self.graph.add_node(pn)
        self.nodes[name] = pn
        return
    

    def add_stream(self, name, from_node, into_node, sub_streams=list()):
        if name in self.streams: raise PFS_Key_Duplication_Error('Cannot have multiple streams with the same name')
        stream = Stream(name, from_node, into_node, sub_streams)
        self.streams[name] = stream
        self.graph.add_edge(from_node, into_node, stream=stream)
        return

    
    def get_streams(self):
        return [stream for __, stream in self.streams.items()]

    
    def get_node_streams(self, node):
        inputs = [s for __, s in self.streams.items() if s.into_node == node]
        outputs = [s for __, s in self.streams.items() if s.from_node == node]
        return inputs, outputs
    
    
    def nodal_mass_balance(self, node, component="ALL"):

        if type(node) != ProcessNode: node = self.nodes[node]

        in_strms, out_strms = self.get_node_streams(node)

        # get total inlet mass flow
        inlet_flow = 0
        for s in in_strms:
            if component == "ALL":
                inlet_flow += s.get_flow_rate_kgs()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        inlet_flow += ss.flow_kgs
        
        # get total outlet mass flow
        outlet_flow = 0
        for s in out_strms:
            if component == "ALL":
                outlet_flow += s.get_flow_rate_kgs()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        outlet_flow += ss.flow_kgs
        
        # compare
        discrepency = Symbol('D')
        overall_expression = inlet_flow - outlet_flow + discrepency
        overall_solution = solve(overall_expression, discrepency)
        return str(overall_expression)+" = 0", overall_solution, inlet_flow, outlet_flow

    
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

            
    def fill_nodes(self):
        for stream in self.get_streams():
            if stream not in stream.from_node.streams:
                stream.from_node.add_stream(stream)
            if stream not in stream.into_node.streams:
                stream.into_node.add_stream(stream)
        return

class ProcessNode(object):

    
    def __init__(self, idx, name, n_type, u_type):

        assert type(n_type) is NodeType
        
        self.idx         = idx
        self.name        = name
        self.n_type      = n_type
        self.u_type      = u_type
        self.streams     = list()
        return


    def __repr__(self):
        return f'Node [{self.idx}/{self.n_type}/{self.name}]'


    def add_stream(self, stream):
        assert type(stream) is Stream
        self.streams.append(stream)
        return
