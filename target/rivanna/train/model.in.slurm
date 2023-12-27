#!/usr/bin/env bash

#SBATCH --job-name={identifier}
#SBATCH --output=osmi-{identifier}-%u-%j.out
#SBATCH --error=osmi-{identifier}-%u-%j.err
{slurm.sbatch}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=1
#SBATCH --time={ee.time}

PROGRESS() {
    echo "# ###############################################"
    echo "# cloudmesh status=$1 progress=$2 msg=$3 pid=$$"
    echo "# ###############################################"
}

PROGRESS "running" "configure" 1

#PROJECT_DIR=../../../../..
#MODELS_DIR=$PROJECT_DIR/models

MODELS_DIR=./models

export USER_SCRATCH=/scratch/$USER
# export USER_LOCALSCRATCH=/localscratch/$USER
# export BASE=$USER_SCRATCH
# export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
# export PROJECT=$BASE/osmi
# export EXEC_DIR=$PROJECT/target/rivanna


RESULT_DIR=`pwd`

module purge
module load gcc/11.4.0  openmpi/4.1.4 python/3.11.4
#
# change this to OSMI venv as documented
#
source $USER_SCRATCH/ENV3/bin/activate

# PYTHON_DIR=~OSMI
# source $PYTHON_DIR/bin/activate
echo "============================================================"
echo "PROJECT_ID: {identifier}"
echo "MODELS_DIR: $MODELS_DIR"
echo "MODEL: {experiment.model}"
echo "REPEAT: {experiment.repeat}"

PROGRESS "running" "training" 2

cd $MODELS_DIR
time python train.py {experiment.model}

PROGRESS "completed" "done" 100

