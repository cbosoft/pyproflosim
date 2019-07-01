import pubchempy as pcp

from colours import col
from exception import PFS_Component_Not_Found_Error

class ChemicalComponent:

    def __init__(self, name, idx=0):
        res = pcp.get_compounds(name, 'name')
        if res:
            raise PFS_Component_Not_Found_Error(
                    f'No compounds with name {col["command"]}"{name}"{col["reset"]} found!')
        res = res[idx]
        self.name = res.iupac_name
        self.molecular_weight = res.exact_mass
        self.data = res.to_dict()
