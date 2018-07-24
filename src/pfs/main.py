from pfs.colours import C_CMD, C_OKY, C_USR, C_WNG, C_SCS, C_ALT, C_ERR, C_SPL, C_RST
from pfs.process import Process, ProcessNode
from pfs.stream import Stream, SubStream

def main():
    process = Process()
    for i in range(10):
        process.add_node("_node_")
    print(process)
