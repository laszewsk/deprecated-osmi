#!/usr/bin/env bash

#SBATCH --job-name=o-m-small_lstm-b-1-n-1-g-a100-c-1-1
#SBATCH --output=osmi-test.out
#SBATCH --error=osmi-test.err
#SBATCH --gres=gpu:a100:3
#SBATCH --partition=gpu
#SBATCH --account=bii_dsc_community
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=16G
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00

HAPROXY_CFG_FILE=g-3-haproxy_test.cfg

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
echo HAPROXY_CFG_FILE $HAPROXY_CFG_FILE

echo "# ==================================="
echo "# START TF_SERVING"
echo "# ==================================="

mkdir -p ./outputs
CUDA_VISIBLE_DEVICES=0 singularity exec --bind `pwd`:/home --pwd /home image-singularity/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf > outputs/g-3-a100_test_0.log 2>&1 &
CUDA_VISIBLE_DEVICES=1 singularity exec --bind `pwd`:/home --pwd /home image-singularity/serving_latest-gpu.sif tensorflow_model_server --port=8501 --rest_api_port=0 --model_config_file=models.conf > outputs/g-3-a100_test_1.log 2>&1 &
CUDA_VISIBLE_DEVICES=2 singularity exec --bind `pwd`:/home --pwd /home image-singularity/serving_latest-gpu.sif tensorflow_model_server --port=8502 --rest_api_port=0 --model_config_file=models.conf > outputs/g-3-a100_test_2.log 2>&1 &

echo "# ==================================="
echo "# START HAPROXY"
echo "# ==================================="

singularity exec --bind `pwd`:/home --pwd /home image-singularity/osmi.sif python haproxy-cfg-generator.py -p 8500 -g 1 -o $HAPROXY_CFG_FILE -s localhost

singularity exec --bind `pwd`:/home --pwd /home image-singularity/haproxy_latest.sif haproxy -d -f $HAPROXY_CFG_FILE >& outputs/g-3-haproxy_test.log &

sleep 5

echo "# ==================================="
echo "# START CLIENT"
echo "# ==================================="

singularity exec --bind `pwd`:/home --pwd /home image-singularity/osmi.sif python tfs_grpc_client.py localhost:8443 -m small_lstm -b 1024 -n 32678 &> outputs/g-3-small_test.log
