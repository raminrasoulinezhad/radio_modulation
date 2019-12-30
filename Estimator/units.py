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

def from_serial(R, NO_CH=10, BW_IN=2, BW_OUT=8, level=1):

	NO_CYC = int(np.ceil(BW_OUT/BW_IN))
	CNTR_BW = int(np.log2(NO_CYC))

	LUT = CNTR_BW	# comparator + adder

	FF = BW_OUT * NO_CH
	if level > 0:
		FF += 1 		# vld_reg		
		FF += CNTR_BW	# vld_cntr

	BRAM = 0
	DSP = 0
	
	return R + [LUT, FF, BRAM, DSP]

def maxpool_ramin(R, NO_CH=10, BW_IN=12, SER_BW=4, level=1):

	BUF_CYC = 2 * (BW_IN / SER_BW)			
	DATA_SIZE = BW_IN						
	BUF_SIZE = 2 * BW_IN					
	CNTR_SIZE = int(np.ceil(np.log2(BUF_CYC)))
	LATENCY = 3

	LUT = NO_CH * DATA_SIZE		# comparator
	if level > 0:
		LUT += BUF_CYC 			# comparator

	FF = NO_CH * BUF_SIZE		# input_buffer
	FF += NO_CH * BUF_SIZE		# dly
	FF += NO_CH * 1				# max_flag
	FF += NO_CH * BW_IN			# max_x
	if level > 0:
		FF += LATENCY			# vld_sr
		FF += CNTR_SIZE + 1		# cntr_vld

	BRAM = 0
	DSP = 0
	
	return R + [LUT, FF, BRAM, DSP]


def to_serial(R, NO_CH=10, BW_IN=8, BW_OUT=2, level=1):

	NO_CYC = int(np.ceil(BW_IN/BW_OUT))

	LUT = NO_CH * ((BW_IN-BW_OUT)/2)	# shift register circuits
	if level > 0:
		LUT += NO_CYC/2					# reloading vld_sr

	FF = NO_CH * BW_IN 					# tmp_in
	if level > 0:	
		FF += NO_CYC					# vld_sr

	BRAM = 0
	DSP = 0
	
	return R + [LUT, FF, BRAM, DSP]

