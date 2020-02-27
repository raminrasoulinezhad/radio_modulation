# Real-time Automatic Moduation Classification
Classify modulation of signals

This package uses the [twn_generator](https://github.com/da-steve101/twn_generator)
You can install it by running
```bash
pip3 install twn_generator
```
This code was created using python 3.6 and tensorflow 1.14

This project is based on the RFSoC ZCU111 board and the radio modulation dataset created
by [O'Shea et. al](https://arxiv.org/pdf/1712.04578.pdf) available at [deepsig.io](http://opendata.deepsig.io/datasets/2018.01/2018.01.OSC.0001_1024x2M.h5.tar.gz)


The directory [train_tnn](train_tnn) contains all scripts to train the models in tensorflow and extract the weights and various test vectors to csvs.
[models](models) contains the trained models used in this paper and the extracted weights in .csv format.
[scripts](scripts) contains some helper files that create tensorflows .rcrd files from the raw dataset and a verification script using vivado for testing.
[verilog_generation](verilog_generation) has scripts to load the csv weights and generate verilog using the twn_generator package.
[verilog](verilog) contains system verilog files that implement various CNN components needed.
[verilog_test](verilog_test) has a few test benches for verification of the verilog.
[c_generation](c_generation) has scripts to load the the csv weights and generate c code using the twn_generator package.
[c](c) has code to implement quantized cnn components to mimic the precision of the verilog.
It also has files to create a python module for a given model.
[interface_verilog](interface_verilog) It includes the verilog files of a data streamer and required scheduler to connect the Input generator, TWN, and HOST including testbench. The data streamer can generate different modulation signals. 

## Running

#### Verilog
The following command
```bash
./generate_networks.sh
```
will generate all code in c and verilog for all the models.
This code is stored in models/network_name.

For using the verilog model, copy the .sv files from the models directory and the verilog files from [verilog](verilog).
There are three top level modules in [verilog](verilog) which are either the [default twn](verilog/tw_vgg_2iq.sv), for [binary activations](verilog/tw_vgg_2iq_bin.sv)
and for [incremental activations](verilog/tw_vgg_2iq_incr.sv).
They have corresponding testbenches for the [default twn](verilog_test/tw_vgg_2iq_test.sv), for [binary activations](verilog/tw_vgg_2iq_bin_test.sv)
and for [incremental activations](verilog/tw_vgg_2iq_incr_test.sv).

#### C
In the c directory
```bash
export MODEL_DIR=../models/vgg_twn_nu_1.2_0.7_bin_64
python3 setup.py build
```
Will create a loadable python module in build/lib.xxx/pyvgg.xxx.so

If this is in the path it can be loaded and used with
```python
import pyvgg
import numpy as np
# whatever input you want
I_data = np.random.randint( -300, 300, [1024] )
Q_data = np.random.randint( -300, 300, [1024] )
x = np.concatenate( [ I_data, Q_data] ).tolist()
y = pyvgg.compute( x ) # compute the prediction in C
```

To test the quantized performance on all models run
```bash
./test_quant.sh
```

## Citations
```latex
@article{Tridgell:2019:UTN:3361265.3359983,
 author = {Tridgell, Stephen and Kumm, Martin and Hardieck, Martin and Boland, David and Moss, Duncan and Zipf, Peter and Leong, Philip H. W.},
 title = {Unrolling Ternary Neural Networks},
 journal = {ACM Trans. Reconfigurable Technol. Syst.},
 issue_date = {November 2019},
 volume = {12},
 number = {4},
 month = oct,
 year = {2019},
 issn = {1936-7406},
 pages = {22:1--22:23},
 articleno = {22},
 numpages = {23},
 url = {http://doi.acm.org/10.1145/3359983},
 doi = {10.1145/3359983},
 acmid = {3359983},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Low-precision machine learning, sparse matrix operations, ternary neural networks},
} 
```

## cheatsheet:

install (on a GPU system):
	
	pip3 install tensorflow-gpu==1.14 tqdm twn_generator scipy scikit-image

install (on a CPU system):

	pip3 install tensorflow==1.14 tqdm twn_generator scipy scikit-image

tensorboard:

	tensorboard --logdir ramintest_F32_logs/ --port 8080

running: 
	
	python3 run_cnn.py --model_name ../models/ramintest_F32 --dataset /opt/datasets/deepsig/modulation_classification_resnet_train.rcrd --val_dataset /opt/datasets/deepsig/modulation_classification_test_snr_30.rcrd --epochs=10 --batch_size 64 --learning_rate 0.01 --resnet_twn --nu_conv 1.2 --nu_dense 0.7 --gpus 1

generating verilogs:

	cd verilog_generation
	cat generate_tw_vgg10.py
	cat generate_f128.sh
	MODEL_DIR=../models/vgg_twn_nu_1.2_0.7_f128
	rm $MODEL_DIR/*_td*
	time python3 generate_tw_vgg10.py --model_dir $MODEL_DIR --bws_in 16,16,8,4,2,1,1 --bws_out 16,16,8,4,2,1,1 -t n,n,s,s,s,s,s

Forward log to a file:
	
	./script.sh 2>&1 | tee script.rpt

Classes

	0) OOK,
	1) 4ASK,
	2) 8ASK,
	3) BPSK,
	4) QPSK,
	5) 8PSK,
	6) 16PSK,
	7) 32PSK,
	8) 16APSK,
	9) 32APSK,
	10) 64APSK,
	11) 128APSK,
	12) 16QAM,
	13) 32QAM,
	14) 64QAM,
	15) 128QAM,
	16) 256QAM,
	17) AM-SSB-WC,
	18) AM-SSB-SC,
	19) AM-DSB-WC,
	20) AM-DSB-SC,
	21) FM,
	22) GMSK,
	23) OQPSK

Sed (Sid :) 

	cat ./*  | grep "CLB LUTs" | sed -e "s/[^0-9.]/ /g" -e "s/  */ /g" | sed "s/ *//" | sed "s/ /\n/" | sed -n 1~2p

# verification

windower 
windower_ramin:
	ModelSim --> OK
	Estimation --> OK
	windower_ramin is superset of windower

| Module               | Modelsim | estimation |
| :---                 | :---     | :---       |
| windower             | **OK**   | **None**   |
| windower_flex        | **OK**   | **OK**     |
| windower_serial      | **OK**   | **None**   |
| windower_serial_flex | **OK**   | **OK**     |
| to_serial            | **OK**   | **OK**     |
|  |    |      |


# f64 is not working 

ASSERTION FAILED: data_out = 028bff95fa9401e902bd06410ac7096eff9d0130f42df6aa000904d6fff205d0004f018bf779ffc0febe07440aecf7e6, expected_out = 01bb01fc021cfe18ff0aff0efd93fa4ef9bafb47f8b0ff9afcdff99ffd62feb5fe94fe90018c018b07d0025903b3095c

ASSERTION FAILED: data_out = 042d019ffcae038c033907cf0c1005bffef40043f6cef4c2fcba02ef046807d400e600a6f9fa0006ff670a930af7faaa, expected_out = 01bb01fc021cfe18ff0aff0efd93fa4ef9bafb47f8b0ff9afcdff99ffd62feb5fe94fe90018c018b07d0025903b3095c

** Note: $finish    : /home/ramin/test/f64/sim/tw_vgg_2iq_test.sv(61)
Time: 6960 ns  Iteration: 1  Instance: /tw_vgg_2iq_test

