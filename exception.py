from colours import col

class PFS_Error(Exception):
    col['error']+'''Base Error'''+col['reset']


class PFS_Key_Duplication_Error(PFS_Error):
    col['error']+'''Duplicate keys will be generated (try using a different name).'''+col['reset']

    
class PFS_Component_Not_Found_Error(PFS_Error):
    col['error']+'''Could not find the specified compound in the PubChem database'''+col['reset']


def warn(*args, **kwargs):
    coloured_args = [
            col['warn'],
            *args,
            col['reset']
        ]
    print(*coloured_args, **kwargs)
