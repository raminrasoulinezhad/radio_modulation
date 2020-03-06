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

	# to estimate the f64 model
	R_max = set_R_max() 
	R = tw_vgg_2iq()
	logger(R, R_max)
