import os
import argparse
import numpy as np

from utils import *
from units import *

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument( "--level", type=int, default=0, help="The level of accuracy")
	return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	
	R = np.array([0, 0, 0, 0]) #R = LUT, FF, BRAMs, DSP
	R_max = np.array([277400, 554800, 1510, 2020]) #LUT_max, FF_max, BRAM_max, DSP_max

	#R += windower_ramin(WINDOW=7, NO_CH=128) 
	#R += bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=-1, level=1)
	#R += from_serial(NO_CH=10, BW_IN=2, BW_OUT=8, level=1)
	#R += maxpool_ramin(NO_CH=10, BW_IN=12, SER_BW=4, level=1)
	#R += to_serial(NO_CH=10, BW_IN=8, BW_OUT=2, level=1)
	#R += serial_adder(BW=16, level=1)
	#R += pipelined_accumulator (IN_BITWIDTH=8, OUT_BITWIDTH=10, LOG2_NO_IN=1)
	R, P = multiply_accumulate_fp (LOG2_NO_VECS=2, BW_IN=16 ,BW_OUT=16 ,BW_W=2, 
	R_SHIFT=0, DEBUG_FLAG=0, USE_UNSIGNED_DATA=0, NUM_CYC=32)

	logger(R, R_max)
	logger(P, R_max)
	logger(R+P, R_max)
	