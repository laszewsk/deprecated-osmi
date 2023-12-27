#!/usr/bin/env bash

#SBATCH --job-name={identifier}
#SBATCH --output=osmi-{identifier}-%u-%j.out
#SBATCH --error=osmi-{identifier}-%u-%j.err
{slurm.sbatch}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00

PROJECT_DIR=../../../../..
MODELS_DIR=$PROJECT_DIR/models

RESULT_DIR=`pwd`

module purge
module load apptainer gcc/11.2.0 openmpi/4.1.4 python/3.11.1

#
# change this to OSMI venv as documented
#
source $USER_PROJECT/ENV3/bin/activate

# PYTHON_DIR=~OSMI
# source $PYTHON_DIR/bin/activate
echo "============================================================"
echo "PROJECT_ID: {identifier}"
echo "MODELS_DIR: $MODELS_DIR"
echo "MODEL: {experiment.model}"
echo "REPEAT: {experiment.repeat}"

cd $MODELS_DIR
time python train.py {experiment.model} > $RESULT_DIR/log.txt 2>&1

