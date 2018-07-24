class Reaction(object):

    def __init__(self, name, reactants, products, stoichiometry, conditions):
        self.name = name
        self.reactants       = reactants
        self.products       = products
        self.stoichiometry  = stoichiometry
        self.conditions     = conditions

class ChemicalComponent(object):
    
    def __init__(self, key, key_type):
        self.pcpcomp = pcp.get_compounds(key, key_type)[0]
