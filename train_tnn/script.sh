GPU=$0

# effect of residual path
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of fewer convs
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of fewer fcs
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128


# effect of fewer convs and fcs
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=16 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128 --norespath
python3 run_cnn.py --model=resnet_twn --lyr_conv=3 --lyr_fc=2 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=64 --fc_ch=128

# effect of firls Conv size
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=5
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=7
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=9

python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=5 --k_n=5 
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=7 --k_n=7
python3 run_cnn.py --model=resnet_twn --lyr_conv=4 --lyr_fc=3 --nu_conv=1.2 --nu_dense=0.7 --gpus=$GPU --lr=0.01 --conv_ch=32 --fc_ch=128 --k_1=9 --k_n=9
