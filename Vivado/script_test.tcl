# ULTRA96 V2
create_project project . -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/pipelined_accumulator.sv}
add_files -norecurse {../verilog/multiply_accumulate_fp.sv}
add_files -norecurse {../verilog/dense_layer_fp.sv}

create_run synth1 -flow {Vivado synthesis 2018}
create_run synth2 -flow {Vivado synthesis 2018}
create_run synth3 -flow {Vivado synthesis 2018}
create_run synth4 -flow {Vivado synthesis 2018}
create_run synth5 -flow {Vivado synthesis 2018}

reset_run synth1
reset_run synth2
reset_run synth3
reset_run synth4
reset_run synth5

# 1 ###########
set_property top dense_layer_fp [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic INPUT_SIZE=2 -generic NUM_CYC=32 -generic BW_IN=16 -generic BW_OUT=23 -generic BW_W=2 -generic R_SHIFT=0 -generic OUTPUT_SIZE=100
launch_runs synth1 -jobs 8

# 2 ###########
set_property top multiply_accumulate_fp [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic LOG2_NO_VECS=1 -generic BW_IN=16 -generic BW_OUT=23 -generic BW_W=2 -generic R_SHIFT=0 -generic NUM_CYC=32
launch_runs synth2 -jobs 8

exit 

