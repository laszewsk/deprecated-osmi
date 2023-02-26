#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:a100:1
#SBATCH --job-name=train-osmi
#SBATCH --output=%u-%j.out
#SBATCH --error=%u-%j.err
#SBATCH --reservation=bi_fox_dgx
#SBATCH --constraint=a100_80gb

## SBATCH -c 4
## SBATCH --mem=32GB

module load anaconda
conda activate OSMI
# pip install --user -r /project/bii_dsc_community/$USER/osmi/mlcommons-osmi/requirements-rivanna.txt
pip install --user -r /scratch/$USER/osmi/machine/rivanna/requirements-rivanna.txt

# cd /project/bii_dsc_community/$USER/osmi/osmi-bench/models
cd /scratch/$USER/osmi/models
time python train.py small_lstm
time python train.py medium_cnn
time python train.py large_tcnn


cd ..
time singularity pull docker://tensorflow/serving:latest-gpu 

nvidia-smi
