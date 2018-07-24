class PFS_Error(Exception):
    '''Base Error'''


class PFS_Key_Duplication_Error(PFS_Error):
    '''Duplicate keys will be generated (try using a different name).'''
