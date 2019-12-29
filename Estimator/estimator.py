import os
import argparse
import numpy as np


def windower_ramin(R, WINDOW=3, NO_CH=2, LOG2_IMG_SIZE=10, 
	THROUGHPUT=1, PADDDING=True, level=1):
	
	L2_TPUT = int(np.ceil(np.log2(THROUGHPUT)))
	PAD = int( ((WINDOW-1)/2) if PADDDING else 0)
	L2_PAD = int(np.ceil(np.log2(PAD)))

	LUT = NO_CH * THROUGHPUT
	if level > 0:
		LUT += 2 * L2_PAD 				# two comparators 
		LUT += LOG2_IMG_SIZE - L2_TPUT 	# counter adder

	FF = NO_CH * WINDOW 				#window_mem
	if level > 0:
		FF += 2 						# state
		FF += LOG2_IMG_SIZE - L2_TPUT 	# cntr
		FF += L2_PAD + 1 				# remaining
		FF += 1 						# vld_out

	BRAM = 0
	DSP = 0
	
	return R + [LUT, FF, BRAM, DSP]
	
def bn(R, NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, 
	R_SHIFT=6, MAXVAL=-1, level=1):

	BITS_MAX = R_SHIFT if ( R_SHIFT > BW_A ) else BW_A;

	LUT = 0 
	# will be captured by DSP 
	# LUT += BW_OUT * NO_CH
	if level > 0:
		LUT += 0

	FF_i = 1 * BW_OUT 					#relu_i 			
	# will capture by DSP registers: 	mult_i(BW_IN+BITS_MAX), bias_i(BW_IN+BITS_MAX), shift_i(BW_OUT)
	FF_i += (1 if (MAXVAL!=-1) else 0)	# set_max
	FF_i += 1							# set_zero
	FF_i += BW_OUT						# data_out

	FF = FF_i * NO_CH

	if level > 0:
		FF += 4		#vld_sr

	BRAM = 0
	DSP = NO_CH
	
	return R + [LUT, FF, BRAM, DSP]

def log(R, R_max):
	LUT, FF, BRAM, DSP = R 
	LUT_max, FF_max, BRAM_max, DSP_max = R_max
	print("LUT(%d): %d\t FF(%d): %d\tBRAMs(%d): %d\tDSP(%d): %d\t" % 
	(LUT_max, LUT, FF_max, FF, BRAM_max, BRAM, DSP_max, DSP))



def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument( "--level", type=int, default=0, help="The level of accuracy")
	return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	
	R = np.array([0, 0, 0, 0]) #R = LUT, FF, BRAMs, DSP
	R_max = np.array([277400, 554800, 1510, 2020]) #LUT_max, FF_max, BRAM_max, DSP_max

	#for i in range(lyr):
	#	# first Conv
	#	# Conv blocks

	#R = windower_ramin(R, WINDOW=7, NO_CH=128) 
	#R = bn(R, NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, R_SHIFT=6, MAXVAL=-1, level=1)

	log(R, R_max)
	