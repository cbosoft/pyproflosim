import copy

import sympy
import pubchempy as pcp

from sympy import Symbol as smb
from sympy import symbols as smbs
from sympy import solve as slv

verbose = False

class colors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"

class process_node(object):

    type = "blank"
    key = 0
    
    def __init__(self, type, key):
        self.type = type
        self.key = key

    def __str__(self):
        return "[NODE:{}/{}]".format(self.type, self.key)
        

class stream(object):
    
    into_node = 0
    from_node = 0
    name = ""
    sub_streams = list()
    
    def __init__(self, name, from_node, into_node, sub_streams=list()):
        self.name = name
        self.into_node = into_node
        self.from_node = from_node
        self.sub_streams = sub_streams
    
    def __str__(self):
        return "[STREAM \"{}\" FROM {}{}{} TO {}{}{}]".format(self.name, colors.RED, self.from_node, colors.RESET, colors.RED, self.into_node, colors.RESET)
    
    def get_flow_rate(self, units="kgs"):
        total = 0
        for ss in self.sub_streams:
            total += ss.flow_kgs
        
        return total
        
class sub_stream(object):

    component = 0
    flow_kgs = 0
    
    def __init__(self, component, flow_kgs):
        self.component = component
        self.flow_kgs = flow_kgs
    
    def __str__(self):
        flow_prefx = ""
        flow_suffx = ""
        if type(self.flow_kgs) is int or type(self.flow_kgs) is float:
            pass
        else:
            flow_prefx = "[SYMB] <"
            flow_suffx = ">"
        return "[SUB-STREAM OF {} AT {}{}{} KG/S]".format(self.component.upper(), flow_prefx, self.flow_kgs, flow_suffx)
        
class chemical_component(object):

    pcpcomp = 0
    
    def __init__(self, key, key_type):
        self.pcpcomp = pcp.get_compounds(key, key_type)[0]

    def __str__(self):
        return self.pcpcomp
        
class process(object):
    
    global verbose

    chemicals   =   {}
                    
    nodes       =   {}
    
    streams     = list()
    
    unknowns    = list()
                    
    def __init__(self):
        pass
        
    def add_chemical(self, name):
        self.chemicals[name] = chemical_component(name, "name")
        
    def add_nodes(self, name, type):
        self.nodes[name] = process_node(type, name)
    
    def add_stream(self, name, from_node, into_node, sub_streams=[0]*0):
        self.streams.append(stream(name, from_node, into_node, sub_streams))
        
    def populate_streams(self):
        #for each stream, add sub stream for each chemical component
        overall_variables = list(list())
        #temp_single_variables = [0] * 0
        for i in range(0, len(self.streams)):
            overall_variables.append(list())
            for c in self.chemicals.keys():
                overall_variables[i].append(smbs("Mdot_{}_s{}".format(c, self.streams[i].name)))
        
        for i in range(0, len(self.streams)):
            a_list_of_subs = list()
            for j in range(0, len(self.chemicals.keys())):
                a_list_of_subs.append(sub_stream(self.chemicals.keys()[j], overall_variables[i][j]))
            self.streams[i].sub_streams = copy.deepcopy(a_list_of_subs)
        #self.mass_flow_matrix = overall_variables

    def get_node_streams(self, node):
        inputs = list()
        outputs = list()
        for s in self.streams:
            if s.from_node == node:
                outputs.append(s)
            elif s.into_node == node:
                inputs.append(s)
        return inputs, outputs
        
    def overall_mass_balance(self):

        # get total inlet mass flow
        if verbose: print " INPUT SUM"
        inlet_flow = 0
        for s in self.streams:
            if s.from_node.type == "input":
                if verbose: print " \t PROCESSING {}".format(s)
                inlet_flow += s.get_flow_rate()
        
        # get total outlet mass flow
        if verbose: print "\n OUTPUT SUM"
        outlet_flow = 0
        for s in self.streams:
            if s.into_node.type == "output":
                if verbose: print " \t PROCESSING {}".format(s)
                outlet_flow += s.get_flow_rate()
        
        # compare
        if verbose: print "\n OBTAINING EXPRESSION"
        overall_expression = inlet_flow - outlet_flow
        if verbose: print "\n SOLVING EXPRESSION"
        overall_solution = slv(overall_expression)

        if verbose: print "\n OVERALL BALANCE COMPLETE\n\tINPUT - OUTPUT = 0\n\t{}\n\t{}".format(overall_expression, overall_solution)
        return overall_expression, overall_solution, inlet_flow, outlet_flow
        
if __name__ == "__main__":
    # create simple test process:
    #
    # One process input, two outputs, one unit, three streams:
    # a distillation column
    
    proc = process()
    
    # Symbols
    xin, yin, xt, yt, xb, yb = smbs('xin yin xt yt xb yb')
    
    # Load components
    proc.add_chemical("ethanol")
    proc.add_chemical("water")
    
    # Create nodes (input/output/inter)
    proc.add_nodes("inlet", "input")
    proc.add_nodes("tops", "output")
    proc.add_nodes("bottoms", "output")
    proc.add_nodes("still", "inter")
    
    # Create streams
    proc.add_stream(proc.nodes["still"], proc.nodes["inlet"], 
            [
                sub_stream(proc.chemicals['ethanol'], xin),
                sub_stream(proc.chemicals['water'], yin)
            ]
        )
    proc.add_stream(proc.nodes["tops"], proc.nodes["still"], 
            [
                sub_stream(proc.chemicals['ethanol'], xt),
                sub_stream(proc.chemicals['water'], yt)
            ]
        )
    proc.add_stream(proc.nodes["bottoms"], proc.nodes["still"], 
            [
                sub_stream(proc.chemicals['ethanol'], xb),
                sub_stream(proc.chemicals['water'], yb)
            ]
        )
    
    expression, solution, ins, outs = proc.overall_mass_balance()
    
    print "INPUT - OUTPUT = 0\n{} - ({}) = 0\n{}".format(ins, outs, solution)
        