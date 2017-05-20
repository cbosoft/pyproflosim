import copy

import sympy
import pubchempy as pcp

from sympy import Symbol as smb
from sympy import symbols as smbs
from sympy import solve as slv

verbose = False

class colors:
    RED     = "\033[1;31m"  
    BLUE    = "\033[1;34m"
    CYAN    = "\033[1;36m"
    GREEN   = "\033[0;32m"
    RESET   = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"
    GRAY    = "\033[1;30m"
    YELLOW  = "\033[1;33m"
    MAGENTA = "\033[1;35m"
    CRIMSON = "\033[1;38m"

    HT_RED      = "\033[1;41m"
    HT_GREEN    = "\033[1;42m"
    HT_BROWN    = "\033[1;43m"
    HT_BLUE     = "\033[1;44m"
    HT_MAGENTA  = "\033[1;45m"
    HT_CYAN     = "\033[1;46m"
    HT_GRAY     = "\033[1;47m"
    HT_CRIMSON  = "\033[1;48m"

class process_node(object):

    type            = "blank"
    key             = 0
    reactions       = list()
    conversions     = list()
    
    def __init__(self, type, key, reactions=list(), conversions=list()):
        self.type           = type
        self.key            = key
        self.rections       = reactions
        self.conversions    = conversions

    def __str__(self):
        return "{}[NODE:{}:{}]{}".format(colors.RED, self.type, self.key, colors.RESET)

class reaction(object):

    name = ""

    reactants       = list()
    products        = list()
    stoichiometry   = dict()
    conditions      = dict()

    def __init__(self, name, reactants, products, stoichiometry, conditions):
        self.name = name
        self.reactants       = reactants
        self.products       = products
        self.stoichiometry  = stoichiometry
        self.conditions     = conditions
        
    def __str__(self):
        r_string = ""
        p_string = ""
        for r in self.reactants:
            r_string += " {} {} +".format(self.stoichiometry[r], r)
        r_string = r_string[:-1]
        for p in self.products:
            p_string += " {} {} +".format(self.stoichiometry[p], p)
        p_string = p_string[:-2]
        return "{}[RXN:{}->{}]{}".format(colors.GREEN, r_string, p_string, colors.RESET)

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
        return "[STREAM \"{}\" FROM {} TO {}]".format(self.name, self.from_node, self.into_node)
    
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
    
    def nodal_mass_balance(self, node, component="ALL"):
        if isinstance(node, basestring):
            node_v = self.nodes[node]
        else:
            node_v = node

        in_strms, out_strms = self.get_node_streams(node_v)

        if verbose: 
            if component == "ALL":
                print colors.BOLD, "\n TOTAL, NODAL MASS BALANCE", colors.RESET
            else:
                print colors.BOLD, "\n {}, NODAL MASS BALANCE".format(component.upper()), colors.RESET

        # get total inlet mass flow
        if verbose: print colors.BOLD, "\n INPUT SUM", colors.RESET
        inlet_flow = 0
        for s in in_strms:
            if verbose: print " \t PROCESSING {}".format(s)
            if component == "ALL":
                inlet_flow += s.get_flow_rate()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        inlet_flow += ss.flow_kgs
        
        # get total outlet mass flow
        if verbose: print colors.BOLD, "\n OUTPUT SUM", colors.RESET
        outlet_flow = 0
        for s in out_strms:
            if verbose: print " \t PROCESSING {}".format(s)
            if component == "ALL":
                outlet_flow += s.get_flow_rate()
            else:
                for ss in s.sub_streams:
                    if ss.component.lower() == component.lower():
                        outlet_flow += ss.flow_kgs
        
        # compare
        if verbose: print colors.BOLD, "\n OBTAINING EXPRESSION", colors.RESET
        discr = smb('D')
        overall_expression = inlet_flow - outlet_flow + discr
        if verbose: print colors.BOLD, "\n SOLVING EXPRESSION", colors.RESET
        overall_solution = slv(overall_expression, discr)

        if verbose: print colors.BOLD, "\n OVERALL BALANCE COMPLETE", colors.RESET
        if verbose: print "\t{}INPUT{} - {}OUTPUT{} + {}DISCREPENCY{} = 0".format(colors.GREEN, colors.RESET, colors.BLUE, colors.RESET, colors.MAGENTA, colors.RESET)
        if verbose: print "\t{}{}{} - {}({}){} + {}{}{} = 0".format(colors.GREEN, inlet_flow, colors.RESET, colors.BLUE, outlet_flow, colors.RESET, colors.MAGENTA, discr, colors.RESET)
        if verbose:
            the_color = colors.RED
            if overall_solution[0] == 0.0:
                the_color = colors.GREEN
            elif not (overall_solution[0] is float and overall_solution[0] is int):
                the_color = colors.MAGENTA
            elif overall_solution[0] > -1 and overall_solution[0] < 1:
                the_color = colors.YELLOW
            print "\t{}{}{} = {}{}{}".format(colors.MAGENTA, discr, colors.RESET, the_color, overall_solution[0], colors.RESET)
        return overall_expression, overall_solution, inlet_flow, outlet_flow
    
    def overall_mass_balance(self, component="ALL"):
        if verbose: 
            if component == "ALL":
                print colors.BOLD, "\n TOTAL, OVERALL MASS BALANCE", colors.RESET
            else:
                print colors.BOLD, "\n {}, OVERALL MASS BALANCE".format(component.upper()), colors.RESET

        # get total inlet mass flow
        if verbose: print colors.BOLD, "\n INPUT SUM", colors.RESET
        inlet_flow = 0
        for s in self.streams:
            if s.from_node.type == "input":
                if verbose: print " \t PROCESSING {}".format(s)
                if component == "ALL":
                    inlet_flow += s.get_flow_rate()
                else:
                    for ss in s.sub_streams:
                        if ss.component.lower() == component.lower():
                            inlet_flow += ss.flow_kgs
        
        # get total outlet mass flow
        if verbose: print colors.BOLD, "\n OUTPUT SUM", colors.RESET
        outlet_flow = 0
        for s in self.streams:
            if s.into_node.type == "output":
                if verbose: print " \t PROCESSING {}".format(s)
                if component == "ALL":
                    outlet_flow += s.get_flow_rate()
                else:
                    for ss in s.sub_streams:
                        if ss.component.lower() == component.lower():
                            outlet_flow += ss.flow_kgs
        
        # compare
        if verbose: print colors.BOLD, "\n OBTAINING EXPRESSION", colors.RESET
        discr = smb('D')
        overall_expression = inlet_flow - outlet_flow + discr
        if verbose: print colors.BOLD, "\n SOLVING EXPRESSION", colors.RESET
        overall_solution = slv(overall_expression, discr)

        if verbose: print colors.BOLD, "\n OVERALL BALANCE COMPLETE", colors.RESET
        if verbose: print "\t{}INPUT{} - {}OUTPUT{} + {}DISCREPENCY{} = 0".format(colors.GREEN, colors.RESET, colors.BLUE, colors.RESET, colors.MAGENTA, colors.RESET)
        if verbose: print "\t{}{}{} - {}({}){} + {}{}{} = 0".format(colors.GREEN, inlet_flow, colors.RESET, colors.BLUE, outlet_flow, colors.RESET, colors.MAGENTA, discr, colors.RESET)
        if verbose:
            the_color = colors.RED
            if overall_solution[0] == 0.0:
                the_color = colors.GREEN
            elif overall_solution[0] > -1 and overall_solution[0] < 1:
                the_color = colors.YELLOW
            print "\t{}{}{} = {}{}{}".format(colors.MAGENTA, discr, colors.RESET, the_color, overall_solution[0], colors.RESET)
        return overall_expression, overall_solution, inlet_flow, outlet_flow
        
    def print_stream_table(self, filep="NOPE", show=False):
        rows = list()
        rows.append("Compound")
        for i in range(0, len(self.streams)):
            rows[len(rows) - 1] += ",{}".format(self.streams[i].name)
        for i in range(0, len(self.chemicals.keys())):
            rows.append(self.chemicals.keys()[i])
            for s in self.streams:
                rows[len(rows) - 1] += ",{}".format(s.sub_streams[i].flow_kgs)
        if filep == "NOPE":
                pass
        else:
            with open(filep, "w") as csvf:
                for r in rows:
                    csvf.write(r + "\n")
        for r in rows:
            cols = r.split(",")
            row = ""
            for c in cols:
                row += "\t\t  {}".format(c)
            if show: print row

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
        
