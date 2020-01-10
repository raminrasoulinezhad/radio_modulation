#!/usr/bin/zsh

# generate the experiment directory 
exp_dir=experiments_convs
mkdir -p $exp_dir

# copy the model files
codes_dir=$exp_dir/codes
#mkdir $codes_dir
cp -r ./../rt_amc_models $codes_dir

# number of parallel tasks (it does not mean the required number of CPUs)
NUM_CORES=4

#parallel --joblog progress.log --resume --bar --gnu -j${NUM_CORES} --header : \
parallel --bar --gnu -j${NUM_CORES} --header : \
    './experiment.sh {model} {conv} {exp_dir} {codes_dir}'\
    ::: model f64 f96 f128 \
    ::: conv conv1 conv2 conv3 conv4 conv5 conv6 conv7 \
    ::: exp_dir $exp_dir \
    ::: codes_dir $codes_dir
