#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:a100:1
#SBATCH --job-name=large-train-osmi
#SBATCH --output=train-large-osmi-%u-%j.out
#SBATCH --error=train-large-osmi-%u-%j.err
#SBATCH --reservation=bi_fox_dgx
#SBATCH --constraint=a100_80gb

if [ -z "$EXEC_DIR" ]; then
    echo "EXEC_DIR is not set"
    exit 1
fi
export CONTAINER_DIR=$EXEC_DIR/image-apptainer/

module purge
module load apptainer
# module load tensorflow/2.10.0 gcc openmpi python

nvidia-smi

source $BASE/ENV3/bin/activate

# cms gpu watch --gpu=0 --delay=0.5 --dense > $SLURM_JOBID.gpu.log &

cd $BASE/osmi/models

MODEL=large_tcnn
time apptainer exec --nv $CONTAINER_DIR/osmi.sif python train.py $MODEL
