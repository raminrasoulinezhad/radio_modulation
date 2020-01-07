import numpy as np
import warnings
import re

def multiplier_cost (a, b):
	LUT = 0
	DSP = 0

	if ((a==16)&(b==2)):
		LUT += 17 			
	elif ((a==16)&(b==4)):
		LUT += 57
	elif ((a==16)&(b > 8)):
		DSP += 1
	else:	
		raise Exception("BW_IN=%d & BW_W=%d are not supported" % (BW_IN,BW_W))

	return np.array([LUT, 0, 0, DSP])

def windower_ramin(WINDOW=3, NO_CH=2, LOG2_IMG_SIZE=10, 
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
	
	return np.array([LUT, FF, BRAM, DSP])
	
def bn(NO_CH=10, BW_IN=12, BW_A=12, BW_B=12, BW_OUT=12, 
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
	
	return np.array([LUT, FF, BRAM, DSP])

def from_serial(NO_CH=10, BW_IN=2, BW_OUT=8, level=1):

	NO_CYC = int(np.ceil(BW_OUT/BW_IN))
	CNTR_BW = int(np.log2(NO_CYC))

	LUT = CNTR_BW	# comparator + adder

	FF = BW_OUT * NO_CH
	if level > 0:
		FF += 1 		# vld_reg		
		FF += CNTR_BW	# vld_cntr

	BRAM = 0
	DSP = 0
	
	return np.array([LUT, FF, BRAM, DSP])

def maxpool_ramin(NO_CH=10, BW_IN=12, SER_BW=4, level=1):

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
	
	return np.array([LUT, FF, BRAM, DSP])


def to_serial(NO_CH=10, BW_IN=8, BW_OUT=2, level=1):

	NO_CYC = int(np.ceil(BW_IN/BW_OUT))

	LUT = NO_CH * ((BW_IN-BW_OUT)/2)	# shift register circuits
	if level > 0:
		LUT += NO_CYC/2					# reloading vld_sr

	FF = NO_CH * BW_IN 					# tmp_in
	if level > 0:	
		FF += NO_CYC					# vld_sr

	BRAM = 0
	DSP = 0
	
	return np.array([LUT, FF, BRAM, DSP])


def serial_adder(BW=16, level=1):

	LUT = BW  		# adder
	LUT += 1		# logic of carry

	FF = BW 		# data_out_reg
	FF += 1			# carry_reg

	BRAM = 0
	DSP = 0
	
	return np.array([LUT, FF, BRAM, DSP])


def popcount_accumulate ():
	raise Exception ("it is not implemented")

def pipelined_accumulator (IN_BITWIDTH=8, OUT_BITWIDTH=10, LOG2_NO_IN=1):

	warnings.warn("Warning: Inaccurate result (pipelined_accumulator)")

	#INCR_BW = (IN_BITWIDTH + 1) if (IN_BITWIDTH < OUT_BITWIDTH) else IN_BITWIDTH
	INCR_BW = (IN_BITWIDTH + 1) if (IN_BITWIDTH < OUT_BITWIDTH) else OUT_BITWIDTH
	
	NO_IN = 2 ** LOG2_NO_IN

	if LOG2_NO_IN == 0:

		LUT = 2*OUT_BITWIDTH		# adder & mux
		FF = OUT_BITWIDTH		# data_out_reg

		BRAM = 0
		DSP = 0

		return np.array([LUT, FF, BRAM, DSP])

	else:

		LUT = int(NO_IN / 2) * INCR_BW 	# signed adder

		FF = int(NO_IN / 2) * INCR_BW		# intermediate_results
		FF += 1							# new_sum_reg

		BRAM = 0
		DSP = 0

		return np.array([LUT, FF, BRAM, DSP]) + pipelined_accumulator (IN_BITWIDTH=INCR_BW, 
			OUT_BITWIDTH=OUT_BITWIDTH, LOG2_NO_IN=LOG2_NO_IN-1)

def multiply_accumulate_fp (LOG2_NO_VECS=2, BW_IN=16, BW_OUT=16, BW_W=2, 
	R_SHIFT=0, USE_UNSIGNED_DATA=0, NUM_CYC=32, full_precision=True):

	warnings.warn("Warning: Inaccurate result (multiply_accumulate_fp)")

	# This number is designed for full precision
	# The reported number is the maximum resource usage
	#	full_precision = True --> maximum

	NO_VECS = 2 ** LOG2_NO_VECS

	LOG2_NUM_CYC = int(np.ceil(np.log2(NUM_CYC)))
	PACC_IN_BW = BW_W + BW_IN

	if full_precision:
		PACC_OUT_BW = PACC_IN_BW + LOG2_NUM_CYC + LOG2_NO_VECS	#ideal
	else:
		#BW_E = R_SHIFT if (R_SHIFT > BW_W) else BW_W
		#PACC_OUT_BW = BW_E + BW_OUT 							#old
		PACC_OUT_BW = R_SHIFT + BW_OUT

	# multipliers
	temp = multiplier_cost (BW_IN, BW_W)

	LUT = NO_VECS * temp[0]
	DSP = NO_VECS * temp[3]

	FF = NO_VECS * PACC_IN_BW		# mult_res
	FF += 1 						# new_sum_reg

	BRAM = 0

	return np.array([LUT, FF, BRAM, DSP]) + pipelined_accumulator(IN_BITWIDTH=PACC_IN_BW, OUT_BITWIDTH=PACC_OUT_BW, LOG2_NO_IN=LOG2_NO_VECS)

def dense_layer_fp(INPUT_SIZE=4, NUM_CYC=512, BW_IN=16, BW_OUT=16, BW_W=16, 
	R_SHIFT=0, USE_UNSIGNED_DATA=0, OUTPUT_SIZE=128):
	
	warnings.warn("Warning: Inaccurate result (dense_layer_fp)")

	LOG2_NO_VECS = int(np.ceil(np.log2(INPUT_SIZE)))
	VLD_SR_LEN = LOG2_NO_VECS + 3
	LOG2_CYC = int(np.ceil(np.log2(NUM_CYC)))

	LUT = int((OUTPUT_SIZE * INPUT_SIZE * BW_W)/2)	# w_or_zero
	LUT += (3 * LOG2_CYC) 		# comparator and counter 

	FF = OUTPUT_SIZE * BW_OUT  	# res_out
	FF += LOG2_CYC				# cntr
	FF += VLD_SR_LEN			# vld_sr

	BRAM = 0
	DSP = 0

	temp = OUTPUT_SIZE * multiply_accumulate_fp(LOG2_NO_VECS=LOG2_NO_VECS, 
		BW_IN=BW_IN, BW_OUT=BW_OUT, BW_W=BW_W, R_SHIFT=R_SHIFT, 
		NUM_CYC=NUM_CYC, USE_UNSIGNED_DATA=USE_UNSIGNED_DATA, 
		full_precision=False)
	#print("LOG2_NO_VECS: %d, BW_IN: %d, BW_OUT: %d, BW_W: %d, R_SHIFT: %d, NUM_CYC: %d, USE_UNSIGNED_DATA: %d" % (LOG2_NO_VECS,BW_IN,BW_OUT,BW_W,R_SHIFT,NUM_CYC,USE_UNSIGNED_DATA))

	# new_sum register optimizations
	temp -= [0, (OUTPUT_SIZE-1)*(LOG2_NO_VECS+1), 0, 0]
	#temp += [OUTPUT_SIZE*3, 0, 0, 0]

	return np.array([LUT, FF, BRAM, DSP]) + temp

def Conv_estimator(file_add="../rt_amc_models/f64/srcs/conv1.sv", DEBUG=False):

	file = open(file_add, "r")
	
	Width = 16
	zero_s = '\$signed\( %d\'h0 \)' % Width

	REG = 0
	ADD = 0 

	for line in file:

		signed = [m.start() for m in re.finditer('\$signed', line)]
		signed_zero = [m.start() for m in re.finditer(zero_s, line)]

		len_s = len(signed)
		len_sz = len(signed_zero)

		if (len_s != 0) & DEBUG:
			print (line[0:-1])
			print ("signed: %d, signed_zero %d" % (len_s, len_sz))

		if len_s == 3:
			if len_sz == 2:
				REG += 1
			elif len_sz == 1:
				REG += 1
				ADD += 1
			else:
				raise Exception("we don't expect this")
		elif len_s != 0:
			raise Exception("we don't expect this")

		if line[0:3] == "reg":
			#print(line[0:-1])
		
			m = re.match(r"reg \[(?P<reg_size>\d+):0\]\[15:0\] out_(?P<index>\d+);", line)
			#m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", line)
			#m = re.search('(?<=reg) \[(\d+)\:(\d+)', line)
			#m = re.search('(?<=[)\w+', line)
			if m != None:
				#print(m.groupdict())
				temp = int(m.group('reg_size')) + 1
				REG += temp 
			
			#if m.group(0) != None:
			#	print(m.group(0))
			
	LUT = ADD * Width	# tree_ & out_
	
	FF = REG * Width	# tree_
	FF += 6 			# rst_reg
	FF += 7 			# vld_reg

	DSP = 0
	BRAM = 0

	return np.array([LUT, FF, BRAM, DSP])
