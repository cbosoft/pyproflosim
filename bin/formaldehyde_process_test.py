from sympy import Symbol as smb
from pyproflosim import *
import pyproflosim as ppfs

proc = process()

# Load components
proc.add_chemical("nitrogen")
proc.add_chemical("oxygen")
proc.add_chemical("methanol")
proc.add_chemical("formaldehyde")
proc.add_chemical("water")

# Create nodes
## Inputs
proc.add_nodes("node_in_air", "input")
proc.add_nodes("node_in_methanol", "input")
proc.add_nodes("node_in_water", "input")

## Intermediates
proc.add_nodes("node_mix_2_3", "inter")
proc.add_nodes("node_mix_9_1", "inter")
proc.add_nodes("node_R-101", "inter")
proc.add_nodes("node_A-101", "inter")
proc.add_nodes("node_recycle", "inter")

## Outputs
proc.add_nodes("node_out_offgas", "output")
proc.add_nodes("node_out_product", "output")

# Create streams
proc.add_stream("(1)_methanol_inlet", proc.nodes["node_in_methanol"], proc.nodes["node_mix_9_1"])
proc.add_stream("(2)_air_inlet", proc.nodes["node_in_air"], proc.nodes["node_mix_2_3"])
proc.add_stream("(3)_gas_recycle", proc.nodes["node_recycle"], proc.nodes["node_mix_2_3"])
proc.add_stream("(4)_reactor_intake", proc.nodes["node_mix_9_1"], proc.nodes["node_R-101"])
proc.add_stream("(5)_reactor_to_absorber", proc.nodes["node_R-101"], proc.nodes["node_A-101"])
proc.add_stream("(6)_product_outlet", proc.nodes["node_A-101"], proc.nodes["node_out_product"])
proc.add_stream("(7)_water_inlet", proc.nodes["node_in_water"], proc.nodes["node_A-101"])
proc.add_stream("(8)_waste_gas_outlet", proc.nodes["node_recycle"], proc.nodes["node_out_offgas"])
proc.add_stream("(9)_post_pre_mix", proc.nodes["node_mix_2_3"], proc.nodes["node_mix_9_1"])
proc.add_stream("(10)_absorber_recycle", proc.nodes["node_A-101"], proc.nodes["node_A-101"])

proc.populate_streams()

ppfs.verbose = True

proc.streams[0].sub_streams[0].flow_kgs = 3.95
for i in range(1, len(proc.streams[0].sub_streams)):
    proc.streams[0].sub_streams[i].flow_kgs = 0.0

expression, solution, ins, outs = proc.overall_mass_balance()