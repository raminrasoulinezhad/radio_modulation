#! /usr/bin/python3
import os
import tensorflow as tf
import quantization as q

def dense_batch_selu_drop_relu(x, training=False, no_filt=128, nu=None, act_prec=None, bn_en=True, selu_en=False, drop_en=True, drop_rate=0.95, relu_en=False):
	if nu is None:
		cnn = tf.layers.dense(x, 128, kernel_initializer=q.get_initializer())
	else:
		filter_shape = [x.get_shape()[-1], no_filt]
		dense_filter = tf.get_variable("dense", filter_shape)
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

def residual_unit(x, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", opt_ResBlock=False): 
	no_filt = x.get_shape()[-1]
	with tf.variable_scope("res_unit_a"):
		cnn = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding)
		#cnn = tf.layers.conv1d( x, no_filt, 3, padding = "SAME" )
		#cnn = tf.layers.batch_normalization( cnn, training = training )
		#cnn = tf.nn.relu( cnn )
	with tf.variable_scope("res_unit_b"):
		if not opt_ResBlock:
			cnn = conv_batch_relu(cnn, training, no_filt=no_filt, nu=nu, act_prec=None, kernel=kernel, padding=padding, relu_en=False)
			#cnn = tf.layers.conv1d( cnn, no_filt, 3, padding = "SAME" )
			#cnn = tf.layers.batch_normalization( cnn, training = training )

		cnn = cnn + x # shortcut
		cnn = q.relu_q(cnn, act_prec=act_prec)
		#cnn = tf.nn.relu( cnn )
		return cnn

def residual_stack(x, no_filt, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", use_bias=False, opt_ResBlock=False):
	with tf.compat.v1.variable_scope("res_stack_a"):
		cnn = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding, use_bias=use_bias, relu_en=False)
		#cnn = tf.layers.conv1d( x, no_filt, 3, padding = "SAME" )
		#cnn = tf.layers.batch_normalization( cnn, training = training )
	with tf.variable_scope("res_stack_b"):
		cnn = residual_unit(cnn, training=training, opt_ResBlock=opt_ResBlock)
	with tf.variable_scope("res_stack_c"):
		cnn = residual_unit(cnn, training=training, opt_ResBlock=opt_ResBlock)
	cnn = tf.layers.max_pooling1d( cnn, 2, 2 )
	return cnn

def get_net(x, training = False, no_filt=64, remove_mean=True, nu=None, act_prec=None, kernel=3, opt_ResBlock=False):
	kernel = [kernel] * (6+3)
	
	print(nu)
	print(act_prec)
	print(kernel)

	# remove the bias from all examples and make
	if remove_mean:
		mean, var = tf.nn.moments(x, axes=[1])
		mean = tf.expand_dims( mean, 1 )
		mean = tf.tile( mean, [ 1, x.get_shape()[1], 1 ] )
		x = ( x - mean )

	with tf.compat.v1.variable_scope("block_1"):
		cnn = residual_stack(x, no_filt, training=training, nu=nu[0], act_prec=act_prec[0], kernel=kernel[0], opt_ResBlock=opt_ResBlock)
	with tf.compat.v1.variable_scope("block_2"):
		cnn = residual_stack(cnn, no_filt, training=training, nu=nu[1], act_prec=act_prec[1], kernel=kernel[1], opt_ResBlock=opt_ResBlock)
	with tf.compat.v1.variable_scope("block_3"):
		cnn = residual_stack(cnn, no_filt, training=training, nu=nu[2], act_prec=act_prec[2], kernel=kernel[2], opt_ResBlock=opt_ResBlock)
	with tf.compat.v1.variable_scope("block_4"):
		cnn = residual_stack(cnn, no_filt, training=training, nu=nu[3], act_prec=act_prec[3], kernel=kernel[3], opt_ResBlock=opt_ResBlock)
	with tf.compat.v1.variable_scope("block_5"):
		cnn = residual_stack(cnn, no_filt, training=training, nu=nu[4], act_prec=act_prec[4], kernel=kernel[4], opt_ResBlock=opt_ResBlock)
	with tf.compat.v1.variable_scope("block_6"):
		cnn = residual_stack(cnn, no_filt, training=training, nu=nu[5], act_prec=act_prec[5], kernel=kernel[5], opt_ResBlock=opt_ResBlock)

	cnn = tf.layers.flatten(cnn)

	with tf.variable_scope("dense_7"):
		cnn = dense_batch_selu_drop_relu(cnn, training=training, no_filt=128, nu=nu[6], act_prec=act_prec[6])
		#cnn = tf.layers.dense(cnn, 128, kernel_initializer=q.get_initializer())
		#cnn = tf.nn.selu( cnn )
		#dropped = tf.contrib.nn.alpha_dropout( cnn, 0.95 )
		#cnn = tf.where( training, dropped, cnn )

	with tf.variable_scope("dense_8"):
		cnn = dense_batch_selu_drop_relu(cnn, training=training, no_filt=128, nu=nu[7], act_prec=act_prec[7])
		#cnn = tf.layers.dense(cnn, 128, kernel_initializer=q.get_initializer())
		#cnn = tf.nn.selu( cnn )
		#dropped = tf.contrib.nn.alpha_dropout( cnn, 0.95 )
		#cnn = tf.where( training, dropped, cnn )

	with tf.variable_scope("dense_9"):
		pred = tf.layers.dense(cnn, 24)

	return pred
