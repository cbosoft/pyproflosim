class Stream(object):
    
    def __init__(self, name, from_node, into_node, sub_streams=list()):
        self.name = name
        self.into_node = into_node
        self.from_node = from_node
        self.sub_streams = sub_streams

    def __iter__(self):
        return self.sub_streams.__iter__()
        
class SubStream(object):
    
    def __init__(self, component, flow_kgs):
        self.component = component
        self.flow_kgs = flow_kgs
