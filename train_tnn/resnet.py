#! /usr/bin/python3
import tensorflow as tf
import quantization as q
from utils import remover_mean

def dense_batch_selu_drop_relu(x, training=False, no_filt=128, nu=None, act_prec=None, bn_en=True, selu_en=False, drop_en=True, drop_rate=0.95, relu_en=False):
	if nu is None:
		x = tf.layers.dense(x, 128, kernel_initializer=q.get_initializer())
	else:
		filter_shape = [x.get_shape()[-1], no_filt]
		dense_filter = tf.compat.v1.get_variable("dense", filter_shape)
		dense_filter = q.trinarize(dense_filter, nu=nu)
		x = tf.matmul(x, dense_filter)

	if bn_en:
		x = tf.layers.batch_normalization(x, training=training)
	if selu_en:
		x = tf.nn.selu(x)

	if drop_en:
		dropped = tf.contrib.nn.alpha_dropout(x, drop_rate)
		x = tf.where(training, dropped, x)

	if relu_en:
		x = tf.nn.relu(x)
	if act_prec is not None:
		x = q.quant(x, act_prec, shift=not(relu_en))
	return x

def conv_batch_relu(x, training=False, no_filt=64, nu=None, act_prec=None, kernel=3, padding="SAME", use_bias=False, pool_en=False, bn_en=True, relu_en=True):
	if nu is None:
		x = tf.layers.conv1d(x, no_filt, kernel, padding=padding, use_bias=use_bias)
	else:
		filter_shape = [kernel, x.get_shape()[-1], no_filt]
		conv_filter = tf.compat.v1.get_variable("conv_filter", filter_shape)
		conv_filter = q.trinarize(conv_filter, nu=nu )
		x = tf.nn.conv1d(x, conv_filter, 1, padding=padding)
	
	if pool_en:
		x = tf.layers.max_pooling1d(x, 2, 2)
	if bn_en:
		x = tf.layers.batch_normalization(x, training=training)
	if relu_en:
		x = tf.nn.relu(x)
	if act_prec is not None:
		x = q.quant(x, act_prec, shift=not(relu_en))
	return x

def residual_unit(x, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", reslen=2, respath=True): 
	no_filt = x.get_shape()[-1]
	
	with tf.variable_scope("res_unit_fconv"):
		cnn = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding)

	for i in range(reslen):
		with tf.variable_scope("res_unit_conv_%d" % i):
			if i == (reslen-1):
				# act_prec=None ==> a floating foint adder is required
				# maybe I should make it act_prec=16 as well
				cnn = conv_batch_relu(cnn, training, no_filt=no_filt, nu=nu, act_prec=None, kernel=kernel, padding=padding, relu_en=False)
			else:
				cnn = conv_batch_relu(cnn, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding, relu_en=False)
	if respath:
		cnn = cnn + x 
	# this batch norm is added by me 
	cnn = tf.layers.batch_normalization(cnn, training=training) 
	cnn = q.relu_q(cnn, act_prec=act_prec)

	return cnn

def residual_stack(x, no_filt, training=False, nu=None, act_prec=None, kernel=3, padding="SAME", use_bias=False, n_resblock=1, reslen=2, respath=True):
	with tf.compat.v1.variable_scope("NConv"):
		x = conv_batch_relu(x, training, no_filt=no_filt, nu=nu, act_prec=act_prec, kernel=kernel, padding=padding, use_bias=use_bias, relu_en=False)

	for i in range(0,n_resblock):
		with tf.variable_scope("ResBlock_"+str(i)):
			x = residual_unit(x, training=training, reslen=reslen, respath=respath)

	x = tf.layers.max_pooling1d( x, 2, 2 )
	return x

def get_net(x, training = False, no_filt=64, remove_mean=True, nu=None, act_prec=None, kernel=3, n_stack_cnv=4, n_stack_fc=3, n_resblock=1, reslen=2, respath=True):

	print("nu: %s, \nact_prec: %s, \nkernel: %s" % (str(nu),str(act_prec),str(kernel)))
	print (respath)

	# remove the bias from all examples and make
	x = remover_mean(x, remove_mean)

	with tf.compat.v1.variable_scope("FirstConv"):
		x = conv_batch_relu(x, training, no_filt=no_filt, nu=nu[0], act_prec=act_prec[0], kernel=kernel[0])

	for i in range(n_stack_cnv):
		with tf.compat.v1.variable_scope("ResStack_"+str(i)):
			x = residual_stack(x, no_filt, training=training, nu=nu[i+1], act_prec=act_prec[i+1], kernel=kernel[i+1], n_resblock=n_resblock[i], reslen=reslen[i], respath=respath)	

	x = tf.compat.v1.layers.flatten(x)

	for i in range(n_stack_fc):
		with tf.compat.v1.variable_scope("DenseStack_"+str(i)):
			if i == (n_stack_fc - 1):
				x = tf.layers.dense(x, kernel[n_stack_cnv+i])
			else:
				x = dense_batch_selu_drop_relu(x, training=training, no_filt=kernel[1+n_stack_cnv+i], nu=nu[1+n_stack_cnv+i], act_prec=act_prec[1+n_stack_cnv+i])

	return x
