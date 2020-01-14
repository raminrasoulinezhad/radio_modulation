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
