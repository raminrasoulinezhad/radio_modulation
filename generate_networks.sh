#! /bin/bash

mkdir rt_amc_models

mkdir rt_amc_models/bin64
mkdir rt_amc_models/bin64_d512
mkdir rt_amc_models/bin128
mkdir rt_amc_models/f64
mkdir rt_amc_models/f96
mkdir rt_amc_models/f128
mkdir rt_amc_models/incr1
mkdir rt_amc_models/rfsoc

verilog_generation/generate_bin64.sh
verilog_generation/generate_bin64_d512.sh
verilog_generation/generate_bin128.sh
verilog_generation/generate_f64.sh
verilog_generation/generate_f96.sh
verilog_generation/generate_f128.sh
verilog_generation/generate_incr1.sh
verilog_generation/generate_rfsoc.sh

# generate c
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_bin_64 --twn_incr_act 6
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_bin_64_d512 --twn_incr_act 6
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_bin_128 --twn_incr_act 6
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_f64
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_f96
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_f128
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_nu_1.2_0.7_incr1_128 --twn_incr_act 1
python3 c_generation/generate_tw_vgg10.py --model_dir models/vgg_twn_rfsoc_50k_64_d128
