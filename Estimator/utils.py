def logger(R, R_max):
	LUT, FF, BRAM, DSP = R 
	LUT_max, FF_max, BRAM_max, DSP_max = R_max
	print("LUT(%d): %d\t FF(%d): %d\tBRAMs(%d): %d\tDSP(%d): %d\t" % 
	(LUT_max, LUT, FF_max, FF, BRAM_max, BRAM, DSP_max, DSP))
