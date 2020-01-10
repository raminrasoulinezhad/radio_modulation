#!/bin/bash

main_dir=`pwd`
echo $main_dir

model=$1
conv=$2
exp_dir=$3
codes_dir=$4

# creat experiment directory
mkdir -p $exp_dir/$model  #
exp_name=$exp_dir/$model/$conv
mkdir -p $exp_name

# copy the files
cp -r $codes_dir/$model/srcs/$conv.sv  $exp_name/$conv.sv
cp -r $codes_dir/$model/srcs/serial_adder.sv  $exp_name/serial_adder.sv

# copy the tcl file
script_file="baseline_script.tcl"
cp $script_file $exp_name/$script_file
sed	-i "s/conv1/$conv/" $exp_name/$script_file
#sed	-i "s|add_files -norecurse { ./conv1.sv }*|add_files -norecurse { ./$conv.sv }|" $exp_name/$script_file
#sed	-i "s|set_property top conv1 [current_fileset]*| set_property top $conv [current_fileset]|" $exp_name/$script_file

###################################################
# running the experiments
cd $exp_name
/opt/Xilinx/Vivado/2018.2/bin/vivado -mode batch -source ./$script_file 

###################################################
# gathering the results in a results folder
final="final"
final_dir=$main_dir/${exp_dir}${final}
mkdir -p $final_dir

temp_s="project_dir/project_test.runs/synth_test/${conv}_utilization_synth.rpt"
temp_d="${model}${conv}.utilplaced.rpt"
cp -r  ./$temp_s  $final_dir/$temp_d
