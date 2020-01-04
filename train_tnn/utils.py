#! /usr/bin/python3
import tensorflow as tf

def remover_mean(x, remove_mean):
	if remove_mean:
		mean, var = tf.nn.moments(x, axes=[1])
		mean = tf.expand_dims(mean, 1)
		mean = tf.tile(mean, [1, x.get_shape()[1], 1])
		x = (x - mean)
	return x
