#! /usr/bin/python3
import os
import tensorflow as tf
#import logging
#logging.getLogger('tensorflow').disabled = True
import csv
import argparse
import resnet
import Vgg10
from tqdm import tqdm
import quantization as q
import math
import sys

'''
Classes:
0) OOK,
1) 4ASK,
2) 8ASK,
3) BPSK,
4) QPSK,
5) 8PSK,
6) 16PSK,
7) 32PSK,
8) 16APSK,
9) 32APSK,
10) 64APSK,
11) 128APSK,
12) 16QAM,
13) 32QAM,
14) 64QAM,
15) 128QAM,
16) 256QAM,
17) AM-SSB-WC,
18) AM-SSB-SC,
19) AM-DSB-WC,
20) AM-DSB-SC,
21) FM,
22) GMSK,
23) OQPSK
'''

def parse_example( ex, use_teacher = False ):
	ftrs = {
		"signal" : tf.io.FixedLenFeature( shape = [2048 ], dtype = tf.float32 ),
		"label" : tf.io.FixedLenFeature( shape = [ 1 ], dtype = tf.string ),
		"snr" : tf.io.FixedLenFeature( shape = [ 1 ], dtype = tf.int64 )
	}
	if use_teacher:
		ftrs["teacher"] = tf.FixedLenFeature( shape = [24], dtype = tf.float32 )
	parsed_ex = tf.io.parse_single_example( ex, ftrs )
	signal = tf.transpose( tf.reshape( parsed_ex["signal"], ( 2, 1024 ) ) )
	label_char = tf.strings.substr( parsed_ex["label"], 0, 1 )
	label = tf.decode_raw( label_char, out_type=tf.uint8)
	label = tf.reshape( label, [] )
	snr = tf.reshape( parsed_ex["snr"], [] )
	if use_teacher:
		teacher = tf.reshape( parsed_ex["teacher"], ( 24, ) )
		return signal, tf.cast( label, tf.int32 ), snr, teacher
	return signal, tf.cast( label, tf.int32 ), snr

def filter_snr_t( signal, label, snr, teacher ):
	return tf.math.greater( snr, 4 )

def filter_snr( signal, label, snr ):
	return tf.math.greater( snr, 4 )

def batcher( input_file, batch_size, training = True, use_teacher = False ):
	dset = tf.data.TFRecordDataset( [ input_file ] )
	dset = dset.map( lambda x: parse_example( x, use_teacher and training ) )
	dset = dset.prefetch( buffer_size = 16*batch_size)
	if training:
		if use_teacher:
			dset = dset.filter( filter_snr_t )
		else:
			dset = dset.filter( filter_snr )
		dset = dset.repeat()
		dset = dset.shuffle(256*batch_size) #8*batch_size q
	dset = dset.batch( batch_size )
	if training:
		iterator = dset.make_initializable_iterator()
	else:
		iterator = dset.make_one_shot_iterator()
	return iterator

def get_optimizer( pred, label, learning_rate, resnet_pred = None ):
	err = tf.nn.sparse_softmax_cross_entropy_with_logits(
		labels = label,
		logits = pred,
		name = "softmax_err_func"
	)
	err = tf.reduce_sum( err )
	tf.compat.v1.summary.scalar( "train_err", err )
	if resnet_pred is not None:
		student_err = tf.sqrt( tf.nn.l2_loss( resnet_pred - pred ) )/5
		tf.summary.scalar( "student_err", student_err )
		err = student_err + err
		teacher_err = tf.nn.sparse_softmax_cross_entropy_with_logits(
			labels = label,
			logits = resnet_pred,
			name = "softmax_teacher_err_func"
		)
		teacher_err = tf.reduce_sum( teacher_err )
		tf.summary.scalar( "teacher_err", teacher_err )
	lr = tf.compat.v1.train.exponential_decay(
		learning_rate,
		tf.compat.v1.train.get_or_create_global_step(),
		100000,
		0.3 #0.5
	)
	
	pred = tf.math.argmax( pred, axis = 1 )
	correct = tf.cast( tf.math.equal( pred, tf.cast( label, tf.int64 ) ), tf.float32 )
	accr = tf.reduce_mean( correct )
	tf.compat.v1.summary.histogram( "preds", pred )
	tf.compat.v1.summary.scalar( "learning_rate", tf.reduce_sum( lr ) )
	tf.compat.v1.summary.scalar( "accuracy", accr )
	update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)
	opt = tf.compat.v1.train.AdamOptimizer( lr )
	with tf.control_dependencies(update_ops):
		return opt.minimize( err, global_step = tf.compat.v1.train.get_or_create_global_step() )

def test_loop(snr, pred, label, training, fname, no_loops, gen_report=False):
	pred = tf.math.argmax( pred, axis = 1 )
	if gen_report:
		if fname is None:
			fname = "test_pred.csv"
		f_out = open( fname, "w" )
		wrt = csv.writer( f_out )

	corr_cnt = 0
	total_cnt = 0
	for i in tqdm(range( no_loops )):
		snr_out, pred_out, label_out = sess.run([snr, pred, label], feed_dict={training:False})
		for s, p, l in zip(snr_out, pred_out, label_out):
			if p == l:
				corr_cnt += 1
			
			if gen_report:
				wrt.writerow([ s, p, l ])
			
			total_cnt += 1

	tf.logging.log( tf.logging.INFO, "Test done, accr = : " + str(corr_cnt/total_cnt) )
	
	if gen_report:
		f_out.close()

def train_loop(opt, smry_wrt, corrects, training, batch_size=32, steps=100000, do_val=True):
	summaries = tf.compat.v1.summary.merge_all()

	curr_step = tf.compat.v1.train.get_global_step()
	step = sess.run(curr_step)
	tf.compat.v1.logging.log(tf.compat.v1.logging.INFO, "Starting train loop at step " + str(step))
	
	steps_log = 10000
	test_size = 410*24
	steps_test = int(math.ceil(test_size/batch_size))

	try:
		for i in range(step, steps):

			step, _, smry = sess.run( [ curr_step, opt, summaries ], feed_dict = { training : True } )

			if (step+1) % 100 == 0:
				smry_wrt.add_summary(smry, step)

			if (step+1) % steps_log == 0 and do_val:
				cnt = 0
				for i in range( steps_test ):
					corr = sess.run(corrects, feed_dict={training:False})
					cnt += corr
				tf.compat.v1.logging.log(tf.compat.v1.logging.INFO, "Step: " + str(step+1) + " - Test accr(snr="+str(snr)+") = " + str(cnt/test_size) )
		
			if (step+1) % epoch_steps == 0 and do_val:
				cnt = 0
				for i in range( steps_test ):
					corr = sess.run( corrects, feed_dict = { training : False } )
					cnt += corr
				tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Epoch("+str(int((step+1) / epoch_steps))+"): accr = " + str(cnt/test_size))

	except KeyboardInterrupt:
		tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Ctrl-c recieved, training stopped" )

	return

def print_conf_mat( preds, labels ):
	classes = ['32PSK', '16APSK', '32QAM', 'FM', 'GMSK',
			   '32APSK', 'OQPSK', '8ASK', 'BPSK', '8PSK',
			   'AM-SSB-SC', '4ASK', '16PSK', '64APSK', '128QAM',
			   '128APSK', 'AM-DSB-SC', 'AM-SSB-WC', '64QAM', 'QPSK',
			   '256QAM', 'AM-DSB-WC', 'OOK', '16QAM']
	print( "\t".join( [ "CM:" ] + classes ) )
	conf_mat = [ [0]*24 for x in range(24) ]
	for p, l in zip( preds, labels ):
		conf_mat[int(p)][int(l)] += 1
	for i, x in enumerate( conf_mat ):
		print( classes[i] + "\t" + ",\t".join( [ str(y) for y in x ]) )

def get_args():
	parser = argparse.ArgumentParser()
	teacher = parser.add_mutually_exclusive_group()
	teacher.add_argument( "--teacher_name", type = str, help="The resnet teacher model to train with")
	teacher.add_argument( "--teacher_dset", action='store_true', help="Use teacher values in the dataset")
	parser.add_argument( "--dataset", type=str, default="/opt/datasets/deepsig/modulation_classification_resnet_train.rcrd",
						 help = "The dataset to train or test on" )
	parser.add_argument( "--val_dataset", type=str, default="/opt/datasets/deepsig/modulation_classification_test_snr_-10.rcrd",
						 help = "The dataset to validate on when training" )
	parser.add_argument( "--steps", type = int, help = "The number of training steps" )
	parser.add_argument( "--epochs", type = int, default=None, help = "The number of training epochs" )
	parser.add_argument( "--test", action = "store_true", help = "Test the model on this dataset" )
	parser.add_argument( "--no_mean", action = "store_true", help = "Do not remove the mean of the signal before processing" )
	parser.add_argument( "--test_output", type = str, help = "Filename to save the output in csv format ( pred, label )" )
	parser.add_argument( "--test_batches", type = int, default = int(math.ceil( 410*24/64)), help = "Number of batches to run on" )
	parser.add_argument( "--batch_size", type=int, default = 64, help = "Batch size to use" )
	parser.add_argument( "--lr", type=float, default = 0.01, help = "The learning rate to use when training" )
	
	parser.add_argument( "--model", type = str, required = True, help="The model name to train or test")
	parser.add_argument("--norespath", action='store_true', help = "disconnect res paths")
	
	
	parser.add_argument( "--fconv_ch", type=int, default=64, help="# of filters in Conv layers" )
	parser.add_argument( "--nu_fconv", type=float, default=None, help = "The parameter to use when trinarizing the conv layers" )
	parser.add_argument( "--act_prec_fconv", type=int, default=None, help="(None or integer) indicating the Activation precision of of the first Conv layer. None = Floatingpoint" )
	parser.add_argument( "--k_1", type=int, default=3, help="kernel size" )

	parser.add_argument("--lyr_conv", type=int, default=4, help = "number of layers Convs")
	parser.add_argument( "--conv_ch", type=int, default=64, help="# of filters in Conv layers" )
	parser.add_argument( "--nu_conv", type=float, default=None, help = "The parameter to use when trinarizing the conv layers" )
	parser.add_argument( "--act_prec_conv", type=int, default=None, help="(None or integer) indicating the Activations precision of Conv layers except the very first one. None = Floatingpoint" )
	parser.add_argument( "--k_n", type=int, default=3, help="kernel size" )
	parser.add_argument( "--n_resblock", type=int, default=1, help="kernel size" )
	parser.add_argument( "--reslen", type=int, default=2, help="kernel size" )

	parser.add_argument("--lyr_fc", type=int, default=3, help = "number of layers FCs")
	parser.add_argument( "--fc_ch", type=int, default=128, help="# of filters in FC layers escept the last one" )
	parser.add_argument( "--nu_dense", type=float, default=None, help = "The parameter to use when trinarizing the dense layers" )
	parser.add_argument( "--act_prec_fc", type=int, default=None, help="(None or integer) indicating the Activations precision of FC layers. None = Floatingpoint" )

	#group = parser.add_mutually_exclusive_group( required = True)
	#group.add_argument("--resnet", action='store_true', help = "Run resnet")
	#group.add_argument("--resnet_twn", action='store_true', help = "Run resnet_twn")
	#group.add_argument("--full_prec", action='store_true', help = "Run full precision VGG with SELU")
	#group.add_argument("--twn", action='store_true', help = "Run Vgg with ternary weights")
	#group.add_argument("--twn_binary_act", action='store_true', help = "Run Vgg with ternary weights and binary activations" )
	parser.add_argument("--twn_incr_act", type=int, help = "Run Vgg with ternary weights and incrementatal precision activations\nInput int the the number of bin act layers from the top, after that double each layer until >= 16\nWhen >= 16 switch to floating point\nWill binaraize the last conv layer and the dense layers" )

	vgg_filt_grp = parser.add_mutually_exclusive_group()
	vgg_filt_grp.add_argument( "--no_filt_vgg", type=int, help = "number of filters to use for vgg" )
	vgg_filt_grp.add_argument( "--no_filts", type=str, help = "number of filters to use for vgg" )

	parser.add_argument( "--gpus", type=str, help = "GPUs to use" )

	return parser.parse_args()

def data_lable_iterator(args, training):
	iterator = batcher( args.dataset, args.batch_size, not args.test, args.teacher_dset )
	test_iterator = None
	do_val = None

	if not args.test:
		if args.teacher_dset:
			train_signal, train_label, train_snr, teacher = iterator.get_next()
		else:
			train_signal, train_label, train_snr = iterator.get_next()

		do_val = True
		if args.val_dataset is not None:
			test_iterator = batcher( args.val_dataset, args.batch_size, not args.test )
			test_signal, test_label, test_snr = test_iterator.get_next()
			signal = tf.where( training, train_signal, test_signal )
			label = tf.where( training, train_label, test_label )
			snr = tf.where( training, train_snr, test_snr )

		else:
			signal, label, snr = ( train_signal, train_label, train_snr )
			do_val = False
	else:
		signal, label, snr = iterator.get_next()

	return iterator, test_iterator, do_val, signal, label, snr

def network_gen(args, signal, training):

	nu = [0.7] + [args.nu_conv]*6 + [args.nu_dense]*2
	no_filt = 64
	if args.no_filt_vgg is not None:
		no_filt = args.no_filt_vgg
	if args.no_filts is not None:
		no_filt = [ int(x) for x in args.no_filts.split(",") ]


	if args.model == "resnet":
		with tf.variable_scope("teacher"):
			pred = resnet.get_net( signal, training=training, remove_mean=not(args.no_mean) )

	elif args.model == "resnet_twn":
		n_stack_cnv = args.lyr_conv
		n_stack_fc = args.lyr_fc

		kernel = [args.k_1] + [args.k_n] * n_stack_cnv + [128,128,24]
		nu = [args.nu_fconv] + [args.nu_conv] * n_stack_cnv + [args.nu_dense] * n_stack_fc
		act_prec =  [args.act_prec_fconv] + [args.act_prec_conv] * n_stack_cnv + [args.act_prec_fc] * n_stack_fc 		# quantize [0-1] #act_prec = [None]*9 	
		n_resblock = [args.n_resblock] * n_stack_cnv
		reslen = [args.reslen] * n_stack_cnv

		pred = resnet.get_net(signal, training=training, no_filt=args.conv_ch, remove_mean=not args.no_mean, 
			nu=nu, act_prec=act_prec, kernel=kernel, n_stack_cnv=n_stack_cnv, 
			n_stack_fc=n_stack_fc, n_resblock=n_resblock, reslen=reslen, respath=not(args.norespath))

	elif args.model == "full_prec":
		pred = Vgg10.get_net( signal, training, use_SELU=True, act_prec = None, nu = None, no_filt = no_filt, remove_mean = not args.no_mean )
	elif args.model == "twn":
		act_prec = [16]*9 	# quantize [0-1]
		pred = Vgg10.get_net( signal, training, use_SELU=False, act_prec = None, nu = nu, no_filt = no_filt, remove_mean = not args.no_mean )
	elif args.model == "twn_binary_act":
		act_prec = [1]*9
		pred = Vgg10.get_net( signal, training, use_SELU=False, act_prec = act_prec, nu = nu, no_filt = no_filt, remove_mean = not args.no_mean )
	elif args.model == "twn_incr_act":
		# last conv and dense layers should be bin
		act_prec = [1]*args.twn_incr_act + [ 1 << ( i + 1 ) for i in range(6-args.twn_incr_act) ] + [1]*3
		act_prec = [ x if x < 16 else None for x in act_prec ]
		pred = Vgg10.get_net( signal, training, use_SELU = False, act_prec = act_prec, nu = nu, no_filt = no_filt, remove_mean = not args.no_mean )
	else:
		tf.compat.v1.logging.log( tf.compat.v1.logging.ERROR, "Invalid arguments" )
		exit()

	return pred

if __name__ == "__main__":
	args = get_args()

	# computing the required steps
	print("****************************************")
	epoch_steps_train = int(24*26*3686/args.batch_size)
	args.steps = epoch_steps_train * args.epochs

	for arg in vars(args):
		print (str(arg) + ": \t"+ str(getattr(args, arg)))
	
	model_dir = ("../models/" + args.model 
		+ "_FConv"
		+ "_" + str(args.fconv_ch) + "Co"
		+ "_" + (("TW_nu%f" % (args.nu_fconv)) if (args.nu_fconv != None) else "FW")
		+ "_Act" + (str(args.act_prec_fconv) if (args.act_prec_fconv != None) else "F")
		+ "_K1st" + str(args.k_1)
		+ "_Convs" + str(args.lyr_conv) 
		+ "_" + str(args.conv_ch) + "Co"
		+ "_" + (("TW_nu%f" % (args.nu_conv)) if (args.nu_conv != None) else "FW")
		+ "_Act" + (str(args.act_prec_conv) if (args.act_prec_conv != None) else "F")
		+ "_Kn" + str(args.k_n)
		+ "_NResB" + str(args.n_resblock)		
		+ "_ResLen" + str(args.reslen)			
		+ "_FCs" + str(args.lyr_fc) 
		+ "_" + str(args.fc_ch) + "Co"
		+ "_" + (("TW_nu%f" % (args.nu_dense)) if (args.nu_dense != None) else "FW")
		+ "_Act" + (str(args.act_prec_fc) if (args.act_prec_fc != None) else "F")
		+ ("_norespath" if (args.norespath and ("resnet" in args.model)) else "")
		)

	print ("directory: " + model_dir)
	print("****************************************")

	
	if args.gpus is not None:
		os.environ["CUDA_VISIBLE_DEVICES"]=args.gpus
	tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.INFO )
	training = tf.compat.v1.placeholder( tf.bool, name = "training" )

	iterator, test_iterator, do_val, signal, label, snr = data_lable_iterator(args, training)

	pred = network_gen(args, signal, training)

	if not args.test:
		pred_label = tf.cast( tf.math.argmax( pred, axis = 1 ), tf.int32 )
		corrects = tf.reduce_sum( tf.cast( tf.math.equal( pred_label, label ), tf.float32 ) )
		corrects = tf.reshape( corrects, [] )

		resnet_pred = None
		if args.teacher_name is not None:
			with tf.variable_scope("teacher"):
				resnet_pred = tf.stop_gradient( resnet.get_net( signal, training = False, remove_mean = not args.no_mean ) )
			resnet_saver = tf.train.Saver( tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="teacher") )
		if args.teacher_dset:
			resnet_pred = teacher
		opt = get_optimizer( pred, label, args.lr, resnet_pred )
	init_op = tf.compat.v1.global_variables_initializer()
	saver = tf.compat.v1.train.Saver()
	tf.compat.v1.summary.histogram( "snr", snr )

	with tf.compat.v1.Session() as sess:
		try:
			if not args.test:
				smry_wrt = tf.compat.v1.summary.FileWriter( model_dir + "_logs", sess.graph, session = sess )
				sess.run( iterator.initializer )
				if do_val:
					sess.run( test_iterator.initializer )
			sess.run( init_op )
			# load the model if possible
			if tf.train.checkpoint_exists( model_dir ):
				tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Loading model ... " )
				saver.restore(sess, model_dir )
			if args.teacher_name is not None and tf.train.checkpoint_exists( args.teacher_name ):
				tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Loading teacher ... " )
				resnet_saver.restore(sess, args.teacher_name )

			if args.test:
				test_loop( snr, pred, label, training, args.test_output, args.test_batches )
			else:
				train_loop(opt, smry_wrt, corrects, training, batch_size=args.batch_size, steps=args.steps, do_val=do_val)#, epoch_steps=epoch_steps_train)

		except tf.errors.OutOfRangeError:
			tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Dataset is finished" )

		finally:
			if not args.test:
				tf.compat.v1.logging.log( tf.compat.v1.logging.INFO, "Saving model ... " )
				saver.save( sess, model_dir )
