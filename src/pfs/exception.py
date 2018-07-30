class PFS_Error(Exception):
    '''Base Error'''


class PFS_Key_Duplication_Error(PFS_Error):
    '''Duplicate keys will be generated (try using a different name).'''

    
class PFS_Component_Not_Found_Error(PFS_Error):
    '''Could not find the specified compound in the PubChem database'''
