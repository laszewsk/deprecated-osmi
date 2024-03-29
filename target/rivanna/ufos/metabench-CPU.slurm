#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii
#SBATCH --account=bii_dsc_community
## SBATCH --gres=gpu:a100
#SBATCH --job-name=train-osmi
#SBATCH --output=%u-%j.out
#SBATCH --error=%u-%j.err
#SBATCH --mem=1G
## SBATCH --reservation=bi_fox_dgx
## SBATCH --constraint=a100_80gb
#SBATCH --mem=1G

## SBATCH -c 4
## SBATCH --mem=32GB

dir="$PROJECT/osmi"
output_dir="$dir/osmi-output"
rivanna="$dir/machine/rivanna"
benchmark="$dir/benchmark"

mkdir -p $output_dir
module load anaconda
conda activate OSMI
pip install --user -r $rivanna/requirements-rivanna.txt
# gpu watch --delay=1 --logfile=$output_dir/gpu-$SLURM_JOB_ID.log --dense

cd $benchmark
singularity run --home `pwd` $dir/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& $output_dir/log &

date
for sec in $(seq -w 10000 -1 1); do
    if [[ $(lsof -i :8500) ]]; then break; fi
done
date

python metabench.py $rivanna/rivanna-CPU.yaml -o $output_dir/cpu-results.csv
