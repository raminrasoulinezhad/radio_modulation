#! /usr/bin/python3

import twn_generator as twn
import Vgg10
import csv
import numpy as np
import tensorflow as tf
import tqdm
import os
import argparse

def run_tf_version( model_name, x_in, nu_conv, nu_dense, no_filt, twn_incr_act = None ):
    x = tf.placeholder( tf.float32, [1,1024,2] )
    nu = [0.7] + [nu_conv]*6 + [nu_dense]*2
    if twn_incr_act is not None:
        act_prec = [1]*twn_incr_act + [ 1 << ( i + 1 ) for i in range(6-twn_incr_act) ] + [1]*3
        act_prec = [ x if x < 16 else None for x in act_prec ]
    else:
        act_prec = None
    vgg_pred = Vgg10.get_net( x, False, act_prec = act_prec, nu = nu, no_filt = no_filt )
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, model_name )
        pred = sess.run( vgg_pred, feed_dict = { x : x_in } )
    return pred

def memoizer_loader( f ):
    prev_outputs = {}
    def helper( fname ):
        if fname not in prev_outputs:
            prev_outputs[fname] = f( fname )
        return prev_outputs[fname]
    return helper

@memoizer_loader
def rd_tri_weights_file( fname ):
    f = open( fname )
    rdr = csv.reader(f)
    data = np.array( [ [ int(x) for x in y ] for y in rdr ] )
    f.close()
    return data

@memoizer_loader
def rd_fp_weights_file( fname ):
    f = open( fname )
    rdr = csv.reader(f)
    data = np.array( [ [ float(x) for x in y ] for y in rdr ] ).astype( np.float32 )
    f.close()
    return data

@memoizer_loader
def rd_bn_file( fname ):
    f = open( fname )
    rdr = csv.reader(f)
    data = np.array( [ [ float(x) for x in y ] for y in rdr ] ).astype( np.float32 )
    f.close()
    return data

def compute_bn_relu( img, bnvars ):
    a = bnvars[0]
    b = bnvars[1]
    if len(bnvars) > 2:
        x_min = bnvars[2]
        x_max = bnvars[3]
        img_min = img <= x_min
        img_max = img >= x_max
    img = a*img + b
    if len(bnvars) > 2:
        img[img_min] = 0
        # note should be the prec needed not 1
        img[img_max] = 1
    return img*(img > 0)

def wr_img( img, fname ):
    f = open( fname, "w" )
    wrt = csv.writer( f )
    for x in img:
        wrt.writerow( x )
    f.close()

def floor_to( img, prec ):
    return np.floor( img * ( 1 << prec ) )/( 1 << prec )

def round_to( img, prec ):
    return np.round( img * ( 1 << prec ) )/( 1 << prec )

def compute_network( model_dir, x_in, no_filt, prec = 4, wr_files = False ):
    img = x_in[0]
    mean = np.mean(img, axis=0)
    img = ( img - mean )
    img = round_to( img, prec )
    for i in range(1,8):
        conv_weights = rd_tri_weights_file( model_dir + "/vgg_conv_lyr" + str(i) + ".csv" )
        conv_weights = np.reshape( conv_weights, [ 3, -1, no_filt ] )
        img = twn.conv1d( img, conv_weights )
        if wr_files:
            wr_img( img, model_dir + "/conv_img_lyr" + str(i) + ".csv" )
        bnvars = rd_bn_file( model_dir + "/vgg_bn_lyr" + str(i) + ".csv" )
        bnvars = round_to( bnvars, prec + 2 )
        img = compute_bn_relu( img, bnvars )
        img = floor_to( img, prec )
        if wr_files:
            wr_img( img, model_dir + "/conv_bn_relu_img_lyr" + str(i) + ".csv" )
        img = twn.maxpool1d( img )
        if wr_files:
            wr_img( img, model_dir + "/conv_mp_img_lyr" + str(i) + ".csv" )
    img = np.reshape( img, [-1] )
    for i in range(1,3):
        dense_weights = rd_tri_weights_file( model_dir + "/vgg_dense_" + str(i) + ".csv" )
        img = np.matmul( img, dense_weights )
        if wr_files:
            wr_img( [img], model_dir + "/dense_img_lyr" + str(i) + ".csv" )
        bnvars = rd_bn_file( model_dir + "/vgg_bn_dense_" + str(i) + ".csv" )
        bnvars = round_to( bnvars, prec + 2 )
        img = compute_bn_relu( img, bnvars )
        img = floor_to( img, prec )
        if wr_files:
            wr_img( [img], model_dir + "/dense_bn_relu_img_lyr" + str(i) + ".csv" )
    dense_weights = rd_fp_weights_file( model_dir + "/vgg_dense_3.csv" )
    if dense_weights.shape[0] != 128: # remove bias row if included
        dense_weights = dense_weights[1:,:]
    img = np.matmul( img, dense_weights )
    if wr_files:
        wr_img( [img], model_dir + "/pred_output.csv" )
    return img

def parse_example( ex ):
    ftrs = {
        "signal" : tf.FixedLenFeature( shape = [2048 ], dtype = tf.float32 ),
        "label" : tf.FixedLenFeature( shape = [ 1 ], dtype = tf.string ),
        "snr" : tf.FixedLenFeature( shape = [ 1 ], dtype = tf.int64 )
    }
    parsed_ex = tf.parse_single_example( ex, ftrs )
    signal = tf.transpose( tf.reshape( parsed_ex["signal"], ( 2, 1024 ) ) )
    label_char = tf.substr( parsed_ex["label"], 0, 1 )
    label = tf.decode_raw( label_char, out_type=tf.uint8)
    label = tf.reshape( label, [] )
    snr = tf.reshape( parsed_ex["snr"], [] )
    return signal, tf.cast( label, tf.int32 ), snr

def load_file( fname ):
    dset = tf.data.TFRecordDataset( fname )
    dset = dset.map( parse_example )
    iterator = dset.make_one_shot_iterator()
    return iterator.get_next()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument( "--model_name", type = str, required = True,
                         help="The model name to train or test")
    parser.add_argument( "--dataset", type = str, nargs = "*",
                         help="The test rcrds to test against")
    parser.add_argument("--twn_incr_act", type=int, default = -1, help =
                        """Run Vgg with ternary weights and incrementatal precision activations
Input int the the number of bin act layers from the top, after that double each layer until >= 16
When >= 16 switch to floating point
Will binaraize the last conv layer and the dense layers""" )
    parser.add_argument( "--nu_conv", type=float, default = 1.2,
                         help = "The parameter to use when trinarizing the conv layers" )
    parser.add_argument( "--nu_dense", type=float, default = 0.7,
                         help = "The parameter to use when trinarizing the dense layers" )
    parser.add_argument( "--no_filt", type=int, default = 64,
                         help = "number of filters to use for vgg" )
    parser.add_argument( "--run_only", type=int, default = -1,
                         help = "number of iter to run, -1 => all" )
    parser.add_argument( "--wr_files", action='store_true',
                         help = "write files stages" )
    parser.add_argument( "--gpus", type=str, default = "",
                         help = "GPUs to use" )
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    os.environ["CUDA_VISIBLE_DEVICES"]=args.gpus
    if args.dataset is not None:
        signal, label, snr = load_file( args.dataset )
        sess = tf.Session()
        cntr_ary = {}
        correct_ary = {}
        f = open( args.model_name + "_results.csv", "w" )
        wrt = csv.writer( f )
        try:
            nIter = 410*24*len(args.dataset)
            if args.run_only > -1:
                nIter = args.run_only
            for i in tqdm.tqdm( range( nIter ) ):
                x_in, y, z = sess.run( [ signal, label, snr ] )
                if args.wr_files:
                    img = x_in
                    mean = np.mean(img, axis=0)
                    img = ( img - mean )
                    img = round_to( img, prec )
                    wr_img( img, args.model_name + "/input_img.csv")
                np_pred = compute_network( args.model_name, [x_in], args.no_filt, wr_files = args.wr_files )
                preds = np.argmax( np_pred )
                if z not in cntr_ary:
                    cntr_ary[z] = 0
                    correct_ary[z] = 0
                cntr_ary[z] += 1
                wrt.writerow( [ preds, y, z ] )
                if preds == y:
                    correct_ary[z] += 1
        finally:
            f.close()
            for z in range( -20, 32, 2 ):
                if z in cntr_ary:
                    print( "accr[" + str(z) + "] = " + str( 100*correct_ary[z]/cntr_ary[z] ) )
    else:
        if os.path.exists( args.model_name + "/input_img.csv" ):
            x_in = rd_fp_weights_file( args.model_name + "/input_img.csv" )
            x_in = np.array([ x_in ])
        else:
            x_in = np.random.normal( 0, 1, [1,1024,2] ).astype( np.float32 )
        tf_pred = run_tf_version( args.model_name, x_in, args.nu_conv, args.nu_dense, args.no_filt, args.twn_incr_act )
        np_pred = compute_network( args.model_name, x_in, args.no_filt, wr_files = args.wr_files )
        print( "tf_pred = ", tf_pred, tf_pred.shape )
        print( "np_pred = ", np_pred, np_pred.shape )
        print( "diff = ", np.abs( tf_pred - np_pred ) )
        print( "sum = ", np.sum( np.abs( tf_pred - np_pred ) ) )
