from sympy import Symbol as smb
from pyproflosim import *
import pyproflosim as ppfs

proc = process()

# == -- == -- == -- == -- == -- == -- ==
# == -- == -- CHEMICAL DATA  -- == -- ==
# == -- == -- from: Process Spec?  -- ==
# == -- == -- == -- == -- == -- == -- ==

# Load components
proc.add_chemical("methanol")
proc.add_chemical("oxygen")
proc.add_chemical("nitrogen")
proc.add_chemical("formaldehyde")
proc.add_chemical("water")

# == -- == -- == -- == -- == -- == -- ==
# == -- == -- PROCESS DATA = -- == -- ==
# == -- == -- from: PF&ID == -- == -- ==
# == -- == -- == -- == -- == -- == -- ==

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

# == -- == -- == -- == -- == -- == -- ==
# == -- == -- STREAM DATA == -- == -- ==
# == -- == -- from: Stream Table = -- ==
# == -- == -- == -- == -- == -- == -- ==

## Stream 1 - methanol inlet
proc.streams[0].sub_streams[0].flow_kgs = 3.9466
for i in range(1, len(proc.streams[0].sub_streams)):
    proc.streams[0].sub_streams[i].flow_kgs = 0.0

## Stream 2 - air inlet
proc.streams[1].sub_streams[0].flow_kgs = 0.0
proc.streams[1].sub_streams[1].flow_kgs = 1.52821
proc.streams[1].sub_streams[2].flow_kgs = 5.208
proc.streams[1].sub_streams[3].flow_kgs = 0.0
proc.streams[1].sub_streams[4].flow_kgs = 0.0

## Stream 3 - gas recycle
proc.streams[2].sub_streams[0].flow_kgs = 0.0
proc.streams[2].sub_streams[1].flow_kgs = 0.4058
proc.streams[2].sub_streams[2].flow_kgs = 24.127
proc.streams[2].sub_streams[3].flow_kgs = 0.0
proc.streams[2].sub_streams[4].flow_kgs = 0.0

## Stream 4
proc.streams[3].sub_streams[0].flow_kgs = 3.9466
proc.streams[3].sub_streams[1].flow_kgs = 1.9728
proc.streams[3].sub_streams[2].flow_kgs = 29.344
proc.streams[3].sub_streams[3].flow_kgs = 0.0
proc.streams[3].sub_streams[4].flow_kgs = 0.0

## Stream 5
proc.streams[4].sub_streams[0].flow_kgs = 0.9856
proc.streams[4].sub_streams[1].flow_kgs = 0.4928
proc.streams[4].sub_streams[2].flow_kgs = 29.344
proc.streams[4].sub_streams[3].flow_kgs = 2.775
proc.streams[4].sub_streams[4].flow_kgs = 1.665

## Stream 6 - product outlet
proc.streams[5].sub_streams[0].flow_kgs = 0.9866
proc.streams[5].sub_streams[1].flow_kgs = 0.0
proc.streams[5].sub_streams[2].flow_kgs = 0.0
proc.streams[5].sub_streams[3].flow_kgs = 2.775
proc.streams[5].sub_streams[4].flow_kgs = 3.7386

## Stream 7
proc.streams[6].sub_streams[0].flow_kgs = 0.0
proc.streams[6].sub_streams[1].flow_kgs = 0.0
proc.streams[6].sub_streams[2].flow_kgs = 0.0
proc.streams[6].sub_streams[3].flow_kgs = 0.0
proc.streams[6].sub_streams[4].flow_kgs = 2.0736

## Stream 8
proc.streams[7].sub_streams[0].flow_kgs = 0.0
proc.streams[7].sub_streams[1].flow_kgs = 0.087
proc.streams[7].sub_streams[2].flow_kgs = 5.2164
proc.streams[7].sub_streams[3].flow_kgs = 0.0
proc.streams[7].sub_streams[4].flow_kgs = 0.0

reactants = ['methanol', 'oxygen']
products = ['formaldehyde', 'water']
stoichiometry = {'methanol':2, 'oxygen':1, 'formaldehyde':2, 'water':2}
conditions = {'T':400}

form_rxn = reaction("catalytic methanol oxidation", reactants, products, stoichiometry, conditions)

print str(form_rxn)

#expression, solution, ins, outs = proc.overall_mass_balance(component="ALL")
#expression, solution, ins, outs = proc.overall_mass_balance(component="methanol")
#expression, solution, ins, outs = proc.overall_mass_balance(component="oxygen")
#expression, solution, ins, outs = proc.overall_mass_balance(component="nitrogen")
#expression, solution, ins, outs = proc.overall_mass_balance(component="formaldehyde")
#expression, solution, ins, outs = proc.overall_mass_balance(component="water")

#expression, solution, ins, outs = proc.nodal_mass_balance("node_A-101", component="ALL")

#proc.print_stream_table(filep="./test.csv")
