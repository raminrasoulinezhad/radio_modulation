import argparse
import numpy as np

from utils import *
from units import *
from units_tb import *

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument( "--level", type=int, default=0, help="The level of accuracy")
	return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	
	R_max = set_R_max() 

	# to estimate the f64 model
	R = tw_vgg_2iq()

	#test()

	logger(R, R_max)
