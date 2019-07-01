import pubchempy
from sympy import Symbol
from sympy import symbols as Symbols
from sympy import solve
from networkx import MultiDiGraph as Graph
from networkx import all_simple_paths
import numpy as np

from pfs.data import components
from pfs.colours import C_CMD, C_OKY, C_USR, C_WNG, C_SCS, C_ALT, C_ERR, C_SPL, C_RST
from pfs.chemical_component import ChemicalComponent
from pfs.exception import PFS_Error, PFS_Key_Duplication_Error
from pfs.types import NodeType, UnitType


class Process(object):
                    

    def __init__(self):
        self.graph      = Graph()
        self.nodes      = dict()
        self.streams    = dict()

        
    def __repr__(self):
        nodes = ''.join('\t'+str(n)+'\n' for n in self.graph.nodes())
        streams = ''.join('\t'+str(data['stream'])+'\n' for __, __, data in self.graph.edges.data())
        return f"Process with nodes:\n{nodes}streams:\n{streams}"

    def __next__(self):
        for edge in self.graph.edges():
            yield edge['stream']
        

    def add_component(self, name):
        components[name] = ChemicalComponent(name)
        return
        

    def add_node(self, name, n_type, u_type):

        if name in self.nodes:
            raise PFS_Key_Duplication_Error("Cannot have multiple nodes with the same name!")
        
        idx = len(self.graph)
        self.graph.add_node(ProcessNode(idx, name, n_type, u_type))
        self.nodes[name] = ProcessNode(idx, name, n_type, u_type)
        print(list(self.graph.nodes())[-1])
        print(self.nodes[name])
        print(self.nodes[name] == list(self.graph.nodes())[-1])
        return
    

    def add_stream(self, name, from_node, into_node, sub_streams=dict()):
        if name in self.streams: raise PFS_Key_Duplication_Error('Cannot have multiple streams with the same name')
        stream = Stream(name, from_node, into_node, sub_streams)
        self.streams[name] = stream
        self.graph.add_edge(from_node, into_node, stream=stream)
        return

    
    def get_streams(self):
        return [stream for __, stream in self.streams.items()]


    def has_unknowns(self):
        for __, s in self.streams.items():
            if not len(s.sub_streams): return True
            for name, __ in components.items():
                try:
                    s.sub_streams[name]
                except KeyError:
                    return True
        return False


    def get_unknowns(self):
        unknowns = list()
        for __, s in self.streams.items():
            for name, __ in components.items():
                try:
                    s.sub_streams[name]
                except KeyError:
                    unknowns.append(f"Mdot_{s.name}_{name}")
        return unknowns

    
    def get_node_streams(self, node):
        inputs = [s for __, s in self.streams.items() if s.into_node == node]
        outputs = [s for __, s in self.streams.items() if s.from_node == node]
        return inputs, outputs


    def balance(self, component=None):
        bal_expr = 0
        for i, (__, node) in enumerate(self.nodes.items()):
            expr, __, __, __ = node.balance(component)
            if not bal_expr:
                bal_expr = expr
            else:
                bal_expr += expr
        return bal_expr

            
    def fill_nodes(self):
        # connect streams to nodes
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
        self.streams     = dict()

        if self.n_type == NodeType.INPUT:
            self.streams[name+"_source"] = Stream(name+"_source", None, self)
        elif self.n_type == NodeType.OUTPUT:
            self.streams[name+"_target"] = Stream(name+"_target", self, None)
        return


    def __repr__(self):
        return f'Node [{self.idx}/{self.n_type}/{self.name}]'
    

    def __eq__(self, other):
        if type(self) == type(other):
            return self.streams == other.streams
        else:
            return False


    def add_stream(self, stream):
        assert type(stream) is Stream
        self.streams[stream.name] = stream
        return

    
    def sort_streams(self):
        into_streams = [s for __, s in self.streams.items() if s.into_node == self]
        from_streams = [s for __, s in self.streams.items() if s.from_node == self]
        return into_streams, from_streams


    def get_unknowns(self, component=None):
        knowns = 0
        for __, s in self.streams.items():
            for __, ss in s.sub_streams.items():
                if ss.component == component:
                    knowns += 1
        if component is None:
            unknowns = len(components) * len(self.streams) - knowns
        else:
            unknowns = len(self.streams) - knowns
        return unknowns


    def check(self, components):
        pass

    
    def balance(self, component=None):

        into_streams, from_streams = self.sort_streams()

        # get total inlet mass flow
        inlet_flow = 0
        for s in into_streams:
            inlet_flow += s.get_flow_rate_kgs(component)
        
        # get total outlet mass flow
        outlet_flow = 0
        for s in from_streams:
            outlet_flow += s.get_flow_rate_kgs(component)
        
        # Generate expression
        overall_expression = inlet_flow - outlet_flow
        return overall_expression

    
class Stream(object):

    
    def __init__(self, name, from_node, into_node, sub_streams=dict()):
        self.name = name

        assert type(from_node) is ProcessNode or from_node == None
        assert type(into_node) is ProcessNode or into_node == None
        assert type(sub_streams) is dict
        
        self.into_node = into_node if into_node else ProcessNode(0, name+"_source", NodeType.OUTSIDE, UnitType.INLET)
        self.from_node = from_node if from_node else ProcessNode(0, name+"_target", NodeType.OUTSIDE, UnitType.OUTLET)
        
        self.sub_streams = sub_streams

        
    def __iter__(self):
        return self.sub_streams.__iter__()

    
    def __str__(self):
        return f"Stream from [{self.from_node}] to [{self.into_node}] ({len(self.sub_streams)} components)"

    
    def add_component(self, component, flowrate_kgs):
        self.sub_streams[component.name] = SubStream(component, flowrate_kgs)

        
    def get_flow_rate_kgs(self, component=None):
        print(self)
        if component:
            try:
                return self.sub_streams[component.name].flowrate_kgs
            except KeyError:
                return Symbol(f'Mdot_{component.name}_{self.name}')
        else:
            if len(self.sub_streams):
                total = 0.0
                for ss in self.sub_streams:
                    total += ss.flowrate_kgs
                return total
            else:
                return Symbol(f'Mdot_{self.name}')
        
class SubStream(object):
    
    def __init__(self, component, flowrate_kgs):
        self.component = component
        self.flowrate_kgs = flowrate_kgs

