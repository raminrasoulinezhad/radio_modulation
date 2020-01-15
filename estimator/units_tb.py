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

def unit_testers():
	#R += windower_ramin(WINDOW=7, NO_CH=128) 
	#R += bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=-1, level=1)
	#R += from_serial(NO_CH=10, BW_IN=2, BW_OUT=8, level=1)
	#R += maxpool_ramin(NO_CH=10, BW_IN=12, SER_BW=4, level=1)
	#R += to_serial(NO_CH=10, BW_IN=8, BW_OUT=2, level=1)
	#R += serial_adder(BW=16, level=1)
	#R += pipelined_accumulator (IN_BITWIDTH=8, OUT_BITWIDTH=10, LOG2_NO_IN=1)
	#R += multiply_accumulate_fp (LOG2_NO_VECS=2, BW_IN=16, BW_OUT=16, BW_W=2, R_SHIFT=0, USE_UNSIGNED_DATA=0, NUM_CYC=32)
																

	#R += dense_layer_fp (INPUT_SIZE=4, NUM_CYC=512, BW_IN=16, BW_OUT=16, BW_W=16, R_SHIFT=0, USE_UNSIGNED_DATA=0, OUTPUT_SIZE=128)
	
	#R = dense_layer_fp (INPUT_SIZE=4, NUM_CYC=512, BW_IN=16, BW_OUT=16, BW_W=4, R_SHIFT=0, USE_UNSIGNED_DATA=0, OUTPUT_SIZE=128)
	#logger(R, R_max)
	#R = dense_layer_fp (INPUT_SIZE=4, NUM_CYC=512, BW_IN=16, BW_OUT=29, BW_W=4, R_SHIFT=0, USE_UNSIGNED_DATA=0, OUTPUT_SIZE=128)
	#logger(R, R_max)
	#R = dense_layer_fp (INPUT_SIZE=4, NUM_CYC=512, BW_IN=16, BW_OUT=29, BW_W=2, R_SHIFT=0, USE_UNSIGNED_DATA=0, OUTPUT_SIZE=128)
	#logger(R, R_max)

	#conv_tb(R_max)
	return