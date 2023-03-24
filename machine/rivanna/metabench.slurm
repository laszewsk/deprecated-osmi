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

dir="/project/bii_dsc_community/$USER/osmi-scratch/osmi"
rivanna="$dir/machine/rivanna"
benchmark="$dir/benchmark"

module load anaconda
conda activate OSMI
pip install --user -r $rivanna/requirements-rivanna.txt

cd $benchmark
singularity run --nv --home `pwd` $dir/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &

date
for sec in $(seq -w 10000 -1 1); do
    if [[ $(lsof -i :8500) ]]; then break; fi
done
date

python metabench.py $rivanna/rivanna-V100.yaml

nvidia-smi
