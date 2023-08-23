#!/usr/bin/env bash

#SBATCH --job-name=o-m-small_lstm-b-1-n-1-g-a100-c-1-1
#SBATCH --output=osmi-test.out
#SBATCH --error=osmi-test.err
#SBATCH --gres=gpu:a100:1
#SBATCH --partition=gpu
#SBATCH --account=bii_dsc_community
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --mem=16G
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00

echo "# ==================================="
echo "# SLURM info"
echo "# ==================================="

echo USER $USER
echo HOME $HOME
echo cardname a100
echo ngpus 1
echo repeat 1
echo jobno $SLURM_JOB_ID
echo mem 16G
echo USER $USER

echo "# ==================================="
echo "# START TF_SERVING"
echo "# ==================================="


mkdir -p ./outputs
CUDA_VISIBLE_DEVICES=0 singularity exec --bind `pwd`:/home --pwd /home image-singularity/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf > outputs/v100_test.log 2>&1 &

echo "# ==================================="
echo "# START HAPROXY"
echo "# ==================================="

# cat >haproxy_test.cfg <<EOL
# global
#   tune.ssl.default-dh-param 1024
 
# defaults
#   timeout connect 10000ms
#   timeout client 60000ms
#   timeout server 60000ms
 
# frontend fe_https
#   mode tcp
#   bind *:8443 npn spdy/2 alpn h2,http/1.1
#   default_backend be_grpc

# backend be_grpc
#   mode tcp
#   balance roundrobin
#   server tfs0 localhost:8500

# EOL
# cat haproxy_test.cfg

singularity exec --bind `pwd`:/home --pwd /home image-singularity/haproxy_latest.sif haproxy -d -f haproxy_test.cfg >& outputs/haproxy_test.log &

sleep 5

echo "# ==================================="
echo "# START CLIENT"
echo "# ==================================="

singularity exec --bind `pwd`:/home --pwd /home image-singularity/osmi.sif python tfs_grpc_client.py localhost:8443 -m small_lstm -b 1024 -n 32678 &> outputs/small_test.log
