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





def conv_estimator_old(file_add="../rt_amc_models/f64/srcs/conv1.sv", DEBUG=False):

	file = open(file_add, "r")
	
	Width = 16
	zero_s = '\( \$signed\( %d\'h0 \) \)' % Width

	trees = []
	tree_reg = []
	out_tree = []

	for line in file:

		signed_s = [m.start() for m in re.finditer('\( \$signed\(', line)]
		len_s = len(signed_s)

		signed_zero = [m.start() for m in re.finditer(zero_s, line)]
		len_sz = len(signed_zero)

		if line[0:5] == "tree_":
			print(line[0:-1])

			signed_e = signed_s[1:]
			signed_e.append(len(line)-1)
			print(signed_s)
			print(signed_e)

			if len_s == 3:
				if len_sz == 2:

					m = re.match(r"tree_(?P<index>\d+) <=", line[:signed_s[0]])
					if m != None:
						index = int(m.group('index'))
					

					m = re.match(r"\( \$signed\( tree_(?P<index>\d+) \) \)", line[signed_s[0]:signed_e[0]])
					if m != None:
						comp = int(m.group('index'))
						comp += 1
						if line[signed_s[0]-2] == "-":
							comp = comp * (-1)
					
					m = re.match(r"\( \$signed\( in\[(?P<index>\d+)\] \) \)", line[signed_s[0]:signed_e[0]])
					if m != None: 
						comp = int(m.group('index'))
						comp = (comp + 1) * (2**12)
						if line[signed_s[0]-2] == "-":
							comp = comp * (-1)
					
					reg = 1
					if comp < 0:		# It is an assumption
						add = 1
					else:
						add = 0

					trees.append((index, comp, add, reg, True))
					print(index, comp, add, reg, True)

				elif len_sz == 1:
					reg = 1
					add = 1
					index = None
					comp = None
					trees.append((index, comp, add, reg, False))
					print(index, comp, add, reg, False)

				else:
					raise Exception("we don't expect this")
			elif len_s != 0:
				raise Exception("we don't expect this")

		if line[0:3] == "reg":
			m = re.match(r"reg \[(?P<reg_size>\d+):0\]\[15:0\] out_(?P<index>\d+);", line)
			if m != None:
				print(m.groupdict())
				reg_size = int(m.group('reg_size')) + 1
				tree_i = int(m.group('index'))
				tree_reg.append((tree_i,reg_size))

			m = re.match(r"reg \[15:0\] out_(?P<index>\d+);", line)
			if m != None:
				print(m.groupdict())
				tree_i = int(m.group('index'))
				tree_reg.append((tree_i,1))


		if line[0:4] == "out_":
			m = re.match(r"out_(?P<out_index>\d+) \<\= \{ out_(\d+)\[(\d+):(\d+)\], tree_(?P<tree_index>\d+)\};", line)
			if m != None:
				print(m.groupdict())
				out_index = int(m.group('out_index'))
				tree_index = int(m.group('tree_index'))
				out_tree.append((out_index, tree_index))
			m = re.match(r"out_(?P<out_index>\d+) \<\= tree_(?P<tree_index>\d+);", line)
			if m != None:
				print(m.groupdict())
				out_index = int(m.group('out_index'))
				tree_index = int(m.group('tree_index'))
				out_tree.append((out_index, tree_index))

		#if line[0:10] == "assign out":
		#	m = re.match(r"out_(?P<out_index>\d+) \<\= \{ out_(\d+)\[(\d+):(\d+)\], tree_(?P<tree_index>\d+)\};", line)

	for i in trees:
		print(i)

	ADD = sum([add for (index, comp, add, reg, flag) in trees if (flag == False)])
	REG = sum([reg for (index, comp, add, reg, flag) in trees if (flag == False)])
	print(ADD, REG)
	
	tree_comp = [(comp, add) for (index, comp, add, reg, flag) in trees if (flag == True)]
	tree_comp = list(set(tree_comp))
	ADD += sum([add for (comp, add) in tree_comp])

	tree_comp = [(comp, reg) for (index, comp, add, reg, flag) in trees if (flag == True)]
	tree_comp = list(set(tree_comp))
	REG += sum([reg for (comp, reg) in tree_comp])

	 
	for reg_ind, reg_size in tree_reg:
		tree_ind = [tree_index for (out_index, tree_index) in out_tree if (out_index == reg_ind)]
		tree_ind = tree_ind[0]

		comp_tree_ind = [comp for (index, comp, add, reg, flag) in trees if ((index == tree_ind) & (flag == True)) ]
		if len(comp_tree_ind) != 0:
			comp_tree_ind = comp_tree_ind[0]
			if comp_tree_ind != None:
				tree_indexs_same_comp = [index for (index, comp, add, reg, flag) in trees if ((comp == comp_tree_ind) & (flag == True)) ]
				print(tree_indexs_same_comp)
				reg_indexs = [out_index for (out_index, tree_index) in out_tree if (tree_index in tree_indexs_same_comp)]
				reg_sizes = [reg_size for (reg_ind, reg_size) in tree_reg if (reg_ind in reg_indexs) ]
				REG += max(reg_sizes)/len(reg_sizes)

		#	comp_sim_ind = [i for i, e in enumerate(tree_comp) if ((e == comp) & (i > ind))]

		#	if len(comp_sim_ind) == 0:
		#		REG += reg_size
		#	else:
		#		m_cost = max(tree_comp(i)) for i in comp_sim_ind
		#		if m_cost >= comp

	LUT = ADD * Width	# tree_ & out_
	
	FF = int(REG) * Width	# tree_
	FF += 6 			# rst_reg
	FF += 7 			# vld_reg

	DSP = 0.0
	BRAM = 0.0

	return np.array([LUT, FF, BRAM, DSP])


def conv_estimate(K, Cin, Cout, Streams=1, Precision=16, Deep=1):

	Total = K * Cin * Cout * Streams * Precision

	if Deep == 1:
		LUT_facor = 0.06
	elif Deep == 2:
		LUT_facor = 0.15
	else:
		LUT_facor = 0.25

	if Deep == 1:
		FF_facor = 0.06
	elif Deep == 2:
		FF_facor = 0.15
	else:
		FF_facor = 0.25

	LUT = Total * LUT_facor
	FF = Total * FF_facor
	DSP = 0.0
	BRAM = 0.0

	return np.array([LUT, FF, BRAM, DSP])
	