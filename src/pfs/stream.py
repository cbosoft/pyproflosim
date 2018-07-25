from sympy import Symbol

class Stream(object):
    
    def __init__(self, name, from_node, into_node, sub_streams=list()):
        self.name = name
        self.into_node = into_node
        self.from_node = from_node
        self.sub_streams = sub_streams

    def __iter__(self):
        return self.sub_streams.__iter__()

    def __str__(self):
        return f"Stream from [{self.from_node}] to [{self.into_node}] ({len(self.sub_streams)} components)"

    def add_component(self, component, flowrate_kgs):
        if component not in [ss.component for ss in self.sub_streams]:
            self.sub_streams.append(SubStream(component, flowrate_kgs))
        else:
            ss = [ss.component for ss in self.sub_streams if ss.component == component][0]
            ss.flowrate_kgs = flowrate_kgs

    def get_flow_rate_kgs(self):
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
