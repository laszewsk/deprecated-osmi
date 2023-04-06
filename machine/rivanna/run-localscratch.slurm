#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00
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

export BASE=/localscratch
export RUN_DIR=$BASE/$USER/osmi
output_dir="$RUN_DIR/osmi-output"
benchmark="$RUN_DIR/benchmark"
rivanna="$RUN_DIR/machine/rivanna"


time mkdir -p $RUN_DIR
time cp -r $PROJECT/osmi $RUN_DIR/..
time cd $RUN_DIR


module load anaconda
conda activate OSMI
time pip install --user -r $rivanna/requirements-rivanna.txt

# nextline you comment out initially and next time you run it to see imapct of energy monitoring
# cms gpu watch --gpu=0 --delay=0.5 --dense > outputs/gpu0.log &

echo "# ======= SERVER START"
cd $benchmark
time singularity run --nv --home `pwd` $RUN_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& $output_dir/log &

date
for sec in $(seq -w 10000 -1 1); do
    if [[ $(lsof -i :8500) ]]; then break; fi
done
date

echo "# ======= SERVER UP"

echo "# ======= START"
time python metabench.py $rivanna/rivanna-A100.yaml -o $output_dir/a100-results.csv
echo "# ======= END"

seff $SLURM_JOB_ID

