# ./script.sh 2>&1 | tee script.rpt
#./script.sh | tee script_new.rpt
GPUS=1
BATCH_SIZE=64
TEST_BATCHES=64

# Floating 16Co
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--lr=0.01 --norespath  --gpus $GPUS

for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

# Floating 32Co
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 \
		--k_1=3 --lyr_conv=4 --conv_ch=32 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--lr=0.01 --norespath  --gpus $GPUS

for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 \
		--k_1=3 --lyr_conv=4 --conv_ch=32 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 16 Co
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=16 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=3 --lyr_conv=4 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS

for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=16 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 32 Co
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=3 --lyr_conv=4 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS

for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS --gpus $GPUS $TEST_ARGS	
done


#TWN 16 Co 3Conv
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=16 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=3 --lyr_conv=3 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=16 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=3 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 32 Co 3Conv
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=3 --lyr_conv=3 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=3 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS --gpus $GPUS $TEST_ARGS	
done


#TWN 16 Co 3Conv - first layer is armed
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=3 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=3 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 32 Co 3Conv - first layer is armed
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=3 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=3 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS --gpus $GPUS $TEST_ARGS	
done

#TWN 16 Co 2Conv - first layer is armed
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=2 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=2 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 32 Co 2Conv - first layer is armed
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=2 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=2 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS --gpus $GPUS $TEST_ARGS	
done

#TWN 16 Co 2Conv - first layer is armed 4FC
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=2 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=4 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=2 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=4 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS $TEST_ARGS	
done

#TWN 32 Co 2Conv - first layer is armed 4FC
date
python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
	--k_1=7 --lyr_conv=2 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
	--n_resblock=1 --reslen=1 --lyr_fc=4 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
	--lr=0.01 --norespath --gpus $GPUS
for snr in {-20..30..2}
do
	TEST_ARGS="--test --dataset /opt/datasets/deepsig/modulation_classification_test_snr_$snr.rcrd"
	python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=7 --lyr_conv=2 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=4 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--lr=0.01 --norespath --gpus $GPUS --gpus $GPUS $TEST_ARGS	
done


exit 0

##########################################
# Guppy

# effect of residual path
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of fewer convs
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of fewer fcs
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128


##########################################
# ProfPhillet 

# effect of fewer convs and fcs
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of firls Conv size
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=5
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=7
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=9

python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=5 --k_n=5 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=7 --k_n=7
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=0 --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=9 --k_n=9



