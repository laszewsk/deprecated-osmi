#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:a100
#SBATCH --job-name=train-osmi
#SBATCH --output=%u-%j.out
#SBATCH --error=%u-%j.err
#SBATCH --reservation=bi_fox_dgx
#SBATCH --constraint=a100_80gb

## SBATCH -c 4
## SBATCH --mem=32GB

nvidia-smi

dir="$PROJECT/osmi"
rivanna="$dir/machine/rivanna"
models="$dir/models"

mkdir -p $output_dir
module load anaconda
conda activate OSMI
pip install --user -r $rivanna/requirements-rivanna.txt

cd $models
time python train.py small_lstm
time python train.py medium_cnn
time python train.py large_tcnn

cd $dir
time singularity pull docker://tensorflow/serving:latest-gpu 
