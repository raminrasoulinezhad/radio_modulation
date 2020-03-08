# ULTRA96 V2
create_project project ./mult_cost -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/mult_cost.v}

create_run synth1 -flow {Vivado synthesis 2018}
create_run synth2 -flow {Vivado synthesis 2018}
create_run synth3 -flow {Vivado synthesis 2018}
create_run synth4 -flow {Vivado synthesis 2018}
create_run synth5 -flow {Vivado synthesis 2018}
create_run synth6 -flow {Vivado synthesis 2018}

reset_run synth1
reset_run synth2
reset_run synth3
reset_run synth4
reset_run synth5
reset_run synth6

# 1 ###########
set_property top mult_cost [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic a_size=16 -generic b_size=2 -generic BW_IN=16 -generic a_v_en=0 -generic b_v_en=0
launch_runs synth1 -jobs 8

# 2 ###########
set_property top mult_cost [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic a_size=16 -generic b_size=4 -generic BW_IN=16 -generic a_v_en=0 -generic b_v_en=0
launch_runs synth2 -jobs 8

# 3 ###########
set_property top mult_cost [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic a_size=16 -generic b_size=2 -generic BW_IN=16 -generic a_v_en=0 -generic b_v_en=1'b1
launch_runs synth3 -jobs 8

# 4 ###########
set_property top mult_cost [current_fileset]
update_compile_order -fileset sources_1
update_compile_order -fileset sources_1
synth_design -generic a_size=16 -generic b_size=4 -generic BW_IN=16 -generic a_v_en=0 -generic b_v_en=1'b1
launch_runs synth4 -jobs 8

exit 

