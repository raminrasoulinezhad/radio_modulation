# ULTRA96 V2
create_project project . -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/pipelined_accumulator.sv}

create_run synth1 -flow {Vivado synthesis 2018}
create_run synth2 -flow {Vivado synthesis 2018}
create_run synth3 -flow {Vivado synthesis 2018}
create_run synth4 -flow {Vivado synthesis 2018}

reset_run synth1
reset_run synth2
reset_run synth3
reset_run synth4

###############
# 1 ###########
###############
set_property top pipelined_accumulator [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

# OUT_BITWIDTH = IN_BITWIDTH + LOG2_NO_IN + loops_of_MAC
synth_design -generic IN_BITWIDTH=8 -generic OUT_BITWIDTH=8 -generic LOG2_NO_IN=1 

launch_runs synth1 -jobs 8
#wait_on_run synth1

###############
# 2 ###########
###############
set_property top pipelined_accumulator [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic IN_BITWIDTH=6 -generic OUT_BITWIDTH=9 -generic LOG2_NO_IN=3 

launch_runs synth2 -jobs 8
#wait_on_run synth2

###############
# 3 ###########
###############
set_property top pipelined_accumulator [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic IN_BITWIDTH=12 -generic OUT_BITWIDTH=12 -generic LOG2_NO_IN=2

launch_runs synth3 -jobs 8
#wait_on_run synth3

###############
# 4 ###########
###############
set_property top pipelined_accumulator [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic IN_BITWIDTH=10 -generic OUT_BITWIDTH=11 -generic LOG2_NO_IN=4 

launch_runs synth4 -jobs 8
#wait_on_run synth4

exit 

