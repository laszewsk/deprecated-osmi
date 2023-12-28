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

nvidia-smi

PROGRESS "running" "configure" 2

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

if [ -z "$EXEC_DIR" ]; then
    echo "EXEC_DIR is not set"
    exit 1
fi
export CONTAINER_DIR=$EXEC_DIR/image-apptainer/

module purge
module load apptainer

#module purge
#module load gcc/11.4.0  openmpi/4.1.4 python/3.11.4
#module load apptainer/1.2.2 tensorflow/2.13.0
#
# change this to OSMI venv as documented
#
#source $USER_SCRATCH/ENV3/bin/activate

# PYTHON_DIR=~OSMI
# source $PYTHON_DIR/bin/activate

MODEL={experiment.model}
CONTAINER=$CONTAINER_DIR/osmi.sif

echo "============================================================"
echo "PROJECT_ID: {identifier}"
echo "MODELS_DIR: $MODELS_DIR"
echo "MODEL: $MODEL"
echo "REPEAT: {experiment.repeat}"

PROGRESS "running" "training" 3

cd $MODELS_DIR

time apptainer exec --nv $CONTAINER python train.py $MODEL

# apptainer run --nv $CONTAINER_DIR/osmi.sif python train.py {experiment.model}

# time python train.py {experiment.model}

PROGRESS "completed" "done" 100

