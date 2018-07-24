class ProcessNode(object):
    
    def __init__(self, type, key, reactions=list(), conversions=list()):
        self.type           = type
        self.key            = key
        self.reactions      = reactions
        self.conversions    = conversions
