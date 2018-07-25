from enum import Enum

class PFS_Enum(Enum):

    def __str__(self):
        return f"{self.name.lower()}"
    
    def __repr__(self):
        return str(self)
    
class NodeType(PFS_Enum):
    INPUT = 0
    INTER = 1
    OUTPUT = 2

class UnitType(PFS_Enum):
    INLET = 0
    OUTLET = 1
    JUNCTION = 2
    REACTOR = 3
    ABSORBER = 4 # and so on
