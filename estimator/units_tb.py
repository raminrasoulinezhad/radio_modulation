import numpy as np

from utils import *
from units import *

def conv_tb(R_max):
	Precision = [16,16,8,4,2,1,1]
	Deep = [1,2,2,2,2,3,3]
	Cin = [2] + [64] * 6
	Cout = [64] * 7

	R = reset_R()
	print("--- Conv layers with file reading ---")
	for i in range(7):
		R_ = conv(file_addr="../rt_amc_models/f64/srcs/conv%d.sv" % (i+1), act_in=Precision[i])
		R += R_
		logger(R_, R_max)
	print("-------")
	logger(R, R_max)
	print("")
	print("")

	print("--- Conv layers with estimation ---")
	R = reset_R()
	for i in range(7):
		R_ = conv(K=3, Cin=Cin[i], Cout=Cout[i], act_in=Precision[i], Deep=Deep[i])
		R += R_
		logger(R_, R_max)
	print("-------")
	logger(R, R_max)

def BRAM_mapper_tb():
	print(BRAM_mapper (512, 512*2))
	print(BRAM_mapper (512, 512*2))
	print(BRAM_mapper (512, 24*16))

######################################
# Tests  #############################
######################################
def test_dense_layer_fp():
	R_max = set_R_max()
	
#	R = dense_layer_fp(INPUT_SIZE=2, NUM_CYC=32, BW_IN=16, BW_OUT=23, 
#			BW_W=2, R_SHIFT=0, OUTPUT_SIZE=100)
#	logger(R, R_max)
#	exit()

	R = dense_layer_fp(INPUT_SIZE=1, NUM_CYC=512, BW_IN=16, BW_OUT=27, 
		BW_W=2, R_SHIFT=0, OUTPUT_SIZE=512)
	logger(R, R_max)
	R = dense_layer_fp(INPUT_SIZE=2, NUM_CYC=512, BW_IN=16, BW_OUT=28, 
		BW_W=2, R_SHIFT=0, OUTPUT_SIZE=512)
	logger(R, R_max)
	R = dense_layer_fp(INPUT_SIZE=4, NUM_CYC=256, BW_IN=16, BW_OUT=28, 
		BW_W=2, R_SHIFT=0, OUTPUT_SIZE=512)
	logger(R, R_max)

	return 

def test_multiply_accumulate_fp():
	R_max = set_R_max()
	# Check: R_SHIFT+BW_OUT < PACC_OUT_BW
	# for full-precision: "BW_OUT + R_SHIFT = BW_W + BW_IN + $clog2(NUM_CYC) + LOG2_NO_VECS"
	R = multiply_accumulate_fp (LOG2_NO_VECS=2, BW_IN=16, BW_OUT=25, BW_W=2, R_SHIFT=0, NUM_CYC=32, en=False)
	logger(R, R_max)
	R = multiply_accumulate_fp (LOG2_NO_VECS=3, BW_IN=16, BW_OUT=25, BW_W=2, R_SHIFT=2, NUM_CYC=64, en=False)
	logger(R, R_max)
	R = multiply_accumulate_fp (LOG2_NO_VECS=4, BW_IN=16, BW_OUT=25, BW_W=2, R_SHIFT=4, NUM_CYC=128, en=False)
	logger(R, R_max)
	R = multiply_accumulate_fp (LOG2_NO_VECS=5, BW_IN=16, BW_OUT=25, BW_W=2, R_SHIFT=6, NUM_CYC=256, en=False)
	logger(R, R_max)
	return 

def test_pipelined_accumulator():
	R_max = set_R_max()
	R = pipelined_accumulator (IN_BITWIDTH=8, OUT_BITWIDTH=8, LOG2_NO_IN=1)
	logger(R, R_max)
	R = pipelined_accumulator (IN_BITWIDTH=6, OUT_BITWIDTH=9, LOG2_NO_IN=3)
	logger(R, R_max)
	R = pipelined_accumulator (IN_BITWIDTH=12, OUT_BITWIDTH=12, LOG2_NO_IN=2)
	logger(R, R_max)
	R = pipelined_accumulator (IN_BITWIDTH=10, OUT_BITWIDTH=11, LOG2_NO_IN=4)
	logger(R, R_max)
	return 

def test_popcount_accumulate():
	R_max = set_R_max()
	R = popcount_accumulate (NO_CH=512, BW_IN=8, BW_OUT=16, CYC_ACC=4, RSHIFT_CYC=1)
	logger(R, R_max)
	R = popcount_accumulate (NO_CH=512, BW_IN=12, BW_OUT=16, CYC_ACC=4, RSHIFT_CYC=1)
	logger(R, R_max)
	R = popcount_accumulate (NO_CH=512, BW_IN=12, BW_OUT=8, CYC_ACC=4, RSHIFT_CYC=1)
	logger(R, R_max)
	R = popcount_accumulate (NO_CH=512, BW_IN=12, BW_OUT=16, CYC_ACC=8, RSHIFT_CYC=1)
	logger(R, R_max)
	return 

def test_bn():
	R_max = set_R_max()
	R = bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=4095)
	logger(R, R_max)
	R = bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=60)
	logger(R, R_max)
	R = bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=64)
	logger(R, R_max)
	R = bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=32)
	logger(R, R_max)
	return 

def test_from_serial():
	R_max = set_R_max()
	R = from_serial(NO_CH=64, BW_IN=4, BW_OUT=8)
	logger(R, R_max)
	R = from_serial(NO_CH=256, BW_IN=2, BW_OUT=8)
	logger(R, R_max)
	R = from_serial(NO_CH=512, BW_IN=4, BW_OUT=32)
	logger(R, R_max)
	R = from_serial(NO_CH=1024, BW_IN=2, BW_OUT=16)
	logger(R, R_max)
	return 

def test_maxpool_flex():
	R_max = set_R_max()
	R = maxpool_flex(NO_CH=10, BW_IN=12, SER_BW=4)
	logger(R, R_max)
	R = maxpool_flex(NO_CH=20, BW_IN=12, SER_BW=4)
	logger(R, R_max)
	R = maxpool_flex(NO_CH=10, BW_IN=64, SER_BW=4)
	logger(R, R_max)
	R = maxpool_flex(NO_CH=10, BW_IN=12, SER_BW=12)
	logger(R, R_max)
	return 

def test_to_serial():
	R_max = set_R_max()
	R = to_serial(NO_CH=32, BW_IN=12, BW_OUT=2)
	logger(R, R_max)
	R = to_serial(NO_CH=128, BW_IN=12, BW_OUT=3)
	logger(R, R_max)
	R = to_serial(NO_CH=8, BW_IN=12, BW_OUT=4)
	logger(R, R_max)
	R = to_serial(NO_CH=32, BW_IN=12, BW_OUT=6)
	logger(R, R_max)
	return 

def test_windower_serial_flex():
	R_max = set_R_max()
	R = windower_serial_flex(NO_CH=32, LOG2_IMG_SIZE=12, WINDOW=3, SER_CYC=16)
	logger(R, R_max)
	R = windower_serial_flex(NO_CH=8, LOG2_IMG_SIZE=10, WINDOW=5, SER_CYC=8)
	logger(R, R_max)
	R = windower_serial_flex(NO_CH=64, LOG2_IMG_SIZE=8, WINDOW=7, SER_CYC=6)
	logger(R, R_max)
	R = windower_serial_flex(NO_CH=128, LOG2_IMG_SIZE=6, WINDOW=9, SER_CYC=4)
	logger(R, R_max)
	return 

def test_windower_flex():
	R_max = set_R_max()
	R = windower_flex(WINDOW=3, NO_CH=128, LOG2_IMG_SIZE=10, THROUGHPUT=1, PADDDING=True)
	logger(R, R_max)
	R = windower_flex(WINDOW=3, NO_CH=128, LOG2_IMG_SIZE=10, THROUGHPUT=2, PADDDING=True)
	logger(R, R_max)
	R = windower_flex(WINDOW=3, NO_CH=128, LOG2_IMG_SIZE=10, THROUGHPUT=2, PADDDING=True)
	logger(R, R_max)
	R = windower_flex(WINDOW=3, NO_CH=128, LOG2_IMG_SIZE=10, THROUGHPUT=2, PADDDING=True)
	logger(R, R_max)
	return 
