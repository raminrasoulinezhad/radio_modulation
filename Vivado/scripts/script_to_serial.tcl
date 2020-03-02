# ULTRA96 V2
create_project project . -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/to_serial.sv}

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
set_property top to_serial [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic NO_CH=32 -generic BW_IN=12 -generic BW_OUT=2

launch_runs synth1 -jobs 8
wait_on_run synth1

###############
# 2 ###########
###############
set_property top to_serial [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic NO_CH=128 -generic BW_IN=12 -generic BW_OUT=3

launch_runs synth2 -jobs 8
wait_on_run synth2

###############
# 3 ###########
###############
set_property top to_serial [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic NO_CH=8 -generic BW_IN=12 -generic BW_OUT=4

launch_runs synth3 -jobs 8
wait_on_run synth3

###############
# 4 ###########
###############
set_property top to_serial [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic NO_CH=32 -generic BW_IN=12 -generic BW_OUT=6

launch_runs synth4 -jobs 8
wait_on_run synth4

exit 

