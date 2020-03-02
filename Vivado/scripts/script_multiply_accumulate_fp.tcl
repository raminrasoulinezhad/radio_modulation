# ULTRA96 V2
create_project project . -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/pipelined_accumulator.sv}
add_files -norecurse {../verilog/multiply_accumulate_fp.sv}

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
set_property top multiply_accumulate_fp [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

# Check: R_SHIFT+BW_OUT < PACC_OUT_BW
# for full-precision: "R_SHIFT = BW_W + BW_IN + $clog2(NUM_CYC) + LOG2_NO_VECS - BW_OUT"
synth_design -generic LOG2_NO_VECS=1 -generic BW_IN=16 -generic BW_OUT=16 -generic BW_W=2 -generic R_SHIFT=8 -generic NUM_CYC=32

launch_runs synth1 -jobs 8
#wait_on_run synth1

###############
# 2 ###########
###############
set_property top multiply_accumulate_fp [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic LOG2_NO_VECS=2 -generic BW_IN=16 -generic BW_OUT=16 -generic BW_W=2 -generic R_SHIFT=9 -generic NUM_CYC=32

launch_runs synth2 -jobs 8
#wait_on_run synth2

###############
# 3 ###########
###############
set_property top multiply_accumulate_fp [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic LOG2_NO_VECS=3 -generic BW_IN=16 -generic BW_OUT=16 -generic BW_W=2 -generic R_SHIFT=10 -generic NUM_CYC=32

launch_runs synth3 -jobs 8
#wait_on_run synth3

###############
# 4 ###########
###############
set_property top multiply_accumulate_fp [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

synth_design -generic LOG2_NO_VECS=4 -generic BW_IN=16 -generic BW_OUT=16 -generic BW_W=2 -generic R_SHIFT=11 -generic NUM_CYC=32

launch_runs synth4 -jobs 8
#wait_on_run synth4

exit 

