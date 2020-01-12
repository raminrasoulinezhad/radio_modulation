# 	same as ULTRA96 family but biggest
create_project project_test ./project_dir -part xczu19eg-ffve1924-1LV-i

# Adding the sources and constrains
add_files -norecurse { ./conv1.sv serial_adder.sv }
update_compile_order -fileset sources_1
#update_compile_order -fileset sources_1
# selec the top module
set_property top conv1 [current_fileset]

############################################
# setting the parameteres (generally are used to expand the Vivado boundaries (limitations))
set_param synth.elaboration.rodinMoreOptions "rt::set_parameter var_size_limit 4194304"
create_run synth_test -flow {Vivado Synthesis 2018}
create_run impl_test -parent_run synth_test -flow {Vivado Implementation 2018}

############################################
# reset the both synthesis and implementation
reset_run impl_test
reset_run synth_test

############################################
# set to not use LUTs as shift registers
set_property STEPS.SYNTH_DESIGN.ARGS.NO_SRLEXTRACT true [get_runs synth_test]

# to run the synthesis without implementation
launch_runs synth_test -jobs 4
wait_on_run synth_test
