#! /usr/bin/python3

import tensorflow as tf

def get_initializer():
    return tf.variance_scaling_initializer(scale=1.0, mode='fan_in')

def quantize( zr, k ):
    scaling = tf.cast( tf.pow( 2.0, k ) - 1, tf.float32 )
    return tf.round( scaling * zr )/scaling

def shaped_relu( x, k = 1.0 ):
    act = tf.clip_by_value( x, 0, 1 )
    quant = quantize( act, k )
    return act  + tf.stop_gradient( quant - act )

def quant(x, act_prec, shift=False):
    if not (shift):
        act = tf.clip_by_value(x, 0, 1)
        quant = quantize(act, act_prec)
    else:
        act = tf.clip_by_value(x, -1, 1)
        quant = quantize((act+1)/2, act_prec)*2 - 1

    return act + tf.stop_gradient(quant - act)

def relu_q (x, act_prec=None):
    if act_prec is None:
        return tf.nn.relu(x)
    else:
        return shaped_relu(x, act_prec)

def trinarize( x, nu = 1.0 ):
    x_shape = x.get_shape()
    thres = nu * tf.reduce_mean(tf.abs(x))
    g_e = tf.cast( tf.greater_equal( x, thres ), tf.float32 )
    l_e = tf.cast( tf.less_equal( x, -thres ), tf.float32 )
    unmasked = tf.multiply( g_e + l_e, x )
    eta = tf.reduce_mean( tf.abs( unmasked ) )
    t_x = tf.multiply( l_e, -eta )
    t_x = t_x + tf.multiply( g_e, eta )
    return x + tf.stop_gradient( t_x - x )
