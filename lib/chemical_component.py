import pubchempy as pcp
from pfs.exception import PFS_Component_Not_Found_Error

class ChemicalComponent(object):

    def __init__(self, name, idx=0):
        res = pcp.get_compounds(name, 'name')
        if not len(res):
            raise PFS_Component_Not_Found_Error(f'No compounds with name \'{name}\' found!')
        res = res[idx]
        self.name = res.iupac_name
        self.molecular_weight = res.exact_mass
        self.data = res.to_dict()
