import numpy as np

def reset_R():
	#R = LUT, FF, BRAMs, DSP
	return np.array([0., 0., 0., 0.])

def set_R_max():
	#LUT_max, FF_max, BRAM_max, DSP_max
	return np.array([277400, 554800, 1510, 2020])

def logger(R, R_max):
	LUT, FF, BRAM, DSP = R 
	LUT_max, FF_max, BRAM_max, DSP_max = R_max
	print("LUT(%d): %d\t FF(%d): %d\tBRAMs(%d): %d\tDSP(%d): %d\t" % 
	(LUT_max, LUT, FF_max, FF, BRAM_max, BRAM, DSP_max, DSP))
