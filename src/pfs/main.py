import networkx as nx

from pfs.colours import C_CMD, C_OKY, C_USR, C_WNG, C_SCS, C_ALT, C_ERR, C_SPL, C_RST
from pfs.process import Process, ProcessNode, NodeType, UnitType
from pfs.stream import Stream, SubStream
from pfs.vis import draw
from pfs.chemical_component import ChemicalComponent

def main():
    print("Creating process...")
    process = Process()

    print("Adding nodes...")
    ### Nodes ###
    process.add_node("air_inlet", NodeType.INPUT, UnitType.INLET)
    process.add_node("methanol_inlet", NodeType.INPUT, UnitType.INLET)
    process.add_node("water_inlet", NodeType.INPUT, UnitType.INLET)

    process.add_node("mix_2_3", NodeType.INTER, UnitType.JUNCTION)
    process.add_node("mix_9_1", NodeType.INTER, UnitType.JUNCTION)
    process.add_node("r101", NodeType.INTER, UnitType.REACTOR)
    process.add_node("a101", NodeType.INTER, UnitType.ABSORBER)
    process.add_node("recycle_split", NodeType.INTER, UnitType.JUNCTION)

    process.add_node("offgas_outlet", NodeType.OUTPUT, UnitType.OUTLET)
    process.add_node("product_outlet", NodeType.OUTPUT, UnitType.OUTLET)

    print("Adding streams...")
    ### Streams ###
    process.add_stream("methanol_inlet", process.nodes["methanol_inlet"], process.nodes["mix_9_1"])
    process.add_stream("air_inlet", process.nodes["air_inlet"], process.nodes["mix_2_3"])
    process.add_stream("gas_recycle", process.nodes["recycle_split"], process.nodes["mix_2_3"])
    process.add_stream("absorber_tops", process.nodes["a101"], process.nodes["recycle_split"])
    process.add_stream("reactor_intake", process.nodes["mix_9_1"], process.nodes["r101"])
    process.add_stream("reactor_to_absorber", process.nodes["r101"], process.nodes["a101"])
    process.add_stream(
        "product_outlet",
        process.nodes["a101"],
        process.nodes["product_outlet"],
        sub_streams=[
            SubStream(ChemicalComponent("methanol"), 0.9866),
            SubStream(ChemicalComponent("formaldehyde"), 2.775),
            SubStream(ChemicalComponent("water"), 3.7386)
        ]
    )
    process.add_stream("water_inlet", process.nodes["water_inlet"], process.nodes["a101"])
    process.add_stream("waste_gas_outlet", process.nodes["recycle_split"], process.nodes["offgas_outlet"])
    process.add_stream("post_pre_mix", process.nodes["mix_2_3"], process.nodes["mix_9_1"])
    process.add_stream("absorber_recycle", process.nodes["a101"], process.nodes["a101"])
    process.fill_nodes()

    #print(process)
    #draw(process, "process.pdf")
    #print(process.graph.number_of_selfloops())

    #process.get_stream("product_outlet").add_component(ChemicalComponent("methanol"), 0.9866)
    #process.get_stream("product_outlet").add_component(ChemicalComponent("formaldehyde"), 2.775)
    #process.get_stream("product_outlet").add_component(ChemicalComponent("water"), 3.7386)
    
    #for s in process.get_streams():
    #    print(s)

    #print(process.streams['water_inlet'])
    print("Taking mass balance over a101")
    expr, sol, inp, out = process.nodal_mass_balance(process.nodes['a101'])
    print(expr)
