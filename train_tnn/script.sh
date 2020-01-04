#python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=None --act_prec_fconv=None \
#		--k_1=3 --lyr_conv=4 --conv_ch=16 --nu_conv=None --act_prec_conv=None --k_n=3 \
#		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=None --act_prec_fc=None \
#		 --gpus=0 --lr=0.01 --norespath

date

python3 run_cnn.py --model=resnet_twn --fconv_ch=32 \
		--k_1=3 --lyr_conv=4 --conv_ch=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		 --gpus=0 --lr=0.01 --norespath
date

python3 run_cnn.py --model=resnet_twn --fconv_ch=32 \
		--k_1=3 --lyr_conv=4 --conv_ch=32 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--gpus=0 --lr=0.01 --norespath
date

python3 run_cnn.py --model=resnet_twn --fconv_ch=64 \
		--k_1=3 --lyr_conv=4 --conv_ch=64 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 \
		--gpus=0 --lr=0.01 --norespath
date

python3 run_cnn.py --model=resnet_twn --fconv_ch=16 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=16 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--gpus=0 --lr=0.01 --norespath
date

python3 run_cnn.py --model=resnet_twn --fconv_ch=32 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=32 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--gpus=0 --lr=0.01 --norespath
date

python3 run_cnn.py --model=resnet_twn --fconv_ch=64 --nu_fconv=1.2 --act_prec_fconv=16 \
		--k_1=3 --lyr_conv=4 --conv_ch=64 --nu_conv=1.2 --act_prec_conv=16 --k_n=3 \
		--n_resblock=1 --reslen=1 --lyr_fc=3 --fc_ch=128 --nu_dense=0.7 --act_prec_fc=16 \
		--gpus=0 --lr=0.01 --norespath
date

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



