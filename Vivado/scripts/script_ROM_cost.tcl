# ULTRA96 V2
create_project project . -part xczu3eg-sbva484-1-e

add_files -norecurse {../verilog/ROM_cost.v}

create_run synth1 -flow {Vivado synthesis 2018}

reset_run synth1

set_property top ROM_cost [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sources_1

launch_runs synth1 -jobs 8

exit 

