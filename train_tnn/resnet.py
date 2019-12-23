#! /usr/bin/python3
import os
import tensorflow as tf
import quantization as q

def remover_mean(x, remove_mean):
	if remove_mean:
		mean, var = tf.nn.moments(x, axes=[1])
		mean = tf.expand_dims(mean, 1)
		mean = tf.tile(mean, [1, x.get_shape()[1], 1])
		x = (x - mean)
	return x

def dense_batch_selu_drop_relu(x, training=False, no_filt=128, nu=None, act_prec=None, bn_en=True, selu_en=False, drop_en=True, drop_rate=0.95, relu_en=False):
	if nu is None:
		cnn = tf.layers.dense(x, 128, kernel_initializer=q.get_initializer())
	else:
		filter_shape = [x.get_shape()[-1], no_filt]
		dense_filter = tf.compat.v1.get_variable("dense", filter_shape)
		dense_filter = q.trinarize(dense_filter, nu=nu)
		cnn = tf.matmul(x, dense_filter)

	if bn_en:
		cnn = tf.layers.batch_normalization(cnn, training=training)
	if selu_en:
		cnn = tf.nn.selu(cnn)

	if drop_en:
		dropped = tf.contrib.nn.alpha_dropout(cnn, drop_rate)
		cnn = tf.where(training, dropped, cnn)

	if relu_en:
		cnn = tf.nn.relu(cnn)
	if act_prec is not None:
		cnn = q.quant(cnn, act_prec, shift=not(relu_en))
	return cnn

def conv_batch_relu(x, training=False, no_filt=128, nu=None, act_prec=None, kernel=3, padding="SAME", use_bias=False, pool_en=False, bn_en=True, relu_en=True):
	if nu is None:
		cnn = tf.layers.conv1d(x, no_filt, kernel, padding=padding, use_bias=use_bias)
	else:
		filter_shape = [kernel, x.get_shape()[-1], no_filt]
		conv_filter = tf.compat.v1.get_variable("conv_filter", filter_shape)
		conv_filter = q.trinarize(conv_filter, nu=nu )
		cnn = tf.nn.conv1d(x, conv_filter, 1, padding=padding)
	
	if pool_en:
		cnn = tf.layers.max_pooling1d(cnn, 2, 2)
	if bn_en:
		cnn = tf.layers.batch_normalization(cnn, training=training)
	if relu_en:
		cnn = tf.nn.relu(cnn)
	if act_prec is not None:
		cnn = q.quant(cnn, act_prec, shift=not(relu_en))
	return cnn

def residual_unit(x, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", opt_ResBlock=False, respath=True): 
	no_filt = x.get_shape()[-1]
	
	with tf.variable_scope("res_unit_0"):
		cnn = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding)

	with tf.variable_scope("res_unit_1"):
		if not opt_ResBlock:
			# act_prec=None ==> a floating foint adder is required
			# maybe I should make it act_prec=16 as well
			cnn = conv_batch_relu(cnn, training, no_filt=no_filt, nu=nu, act_prec=None, kernel=kernel, padding=padding, relu_en=False)

	if respath:
		cnn = cnn + x 
	# this batch norm is added by me 
	cnn = tf.layers.batch_normalization(cnn, training=training) 
	cnn = q.relu_q(cnn, act_prec=act_prec)

	return cnn

def residual_stack(x, no_filt, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", use_bias=False, opt_ResBlock=False, n_convs=3, respath=True):
	with tf.compat.v1.variable_scope("NConv"):
		cnn = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding, use_bias=use_bias, relu_en=False)

	for i in range(0,n_convs-1):
		with tf.variable_scope("ResBlock_"+str(i)):
			cnn = residual_unit(cnn, training=training, opt_ResBlock=opt_ResBlock, respath=respath)

	cnn = tf.layers.max_pooling1d( cnn, 2, 2 )
	return cnn

def get_net(x, training = False, no_filt=64, remove_mean=True, nu=None, act_prec=None, kernel=3, opt_ResBlock=False, n_stack=6, n_convs=3, respath=True):
	
	kernel = [kernel] * (6+3)

	print("nu: %s, \nact_prec: %s, \nkernel: %s" % (str(nu),str(act_prec),str(kernel)))
	print (respath)

	# remove the bias from all examples and make
	cnn = remover_mean(x, remove_mean)

	for i in range(n_stack):
		with tf.compat.v1.variable_scope("ResStack_"+str(i)):
			cnn = residual_stack(cnn, no_filt, training=training, nu=nu[i], act_prec=act_prec[i], kernel=kernel[i], opt_ResBlock=opt_ResBlock, n_convs=n_convs, respath=respath)	

	cnn = tf.compat.v1.layers.flatten(cnn)

	with tf.variable_scope("dense_0"):
		cnn = dense_batch_selu_drop_relu(cnn, training=training, no_filt=128, nu=nu[6], act_prec=act_prec[6])

	with tf.variable_scope("dense_1"):
		cnn = dense_batch_selu_drop_relu(cnn, training=training, no_filt=128, nu=nu[7], act_prec=act_prec[7])

	with tf.variable_scope("dense_2"):
		pred = tf.layers.dense(cnn, 24)

	return pred
