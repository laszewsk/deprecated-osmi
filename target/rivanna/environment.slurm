#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii-gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --account=bii_dsc_community
#SBATCH --job-name=python3-setup
#SBATCH --output=%u-%j.out
#SBATCH --error=%u-%j.err
#SBATCH --mem-per-gpu=64G

start_python_install=`date +%s`
echo start_python_install $start_python_install

export USER_SCRATCH=/scratch/$USER
export BASE=/project/bii_dsc_community/
export USER_PROJECT=$BASE/$USER
# this script requires you to set PROJECT in the command line
export PROJECT_DIR=$PROJECT/osmi
export EXEC_DIR=$PROJECT_DIR/target/rivanna
# export PROJECT_DATA=$USER_SCRATCH/data

mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

module purge
# module load  gcc/9.2.0  cuda/11.0.228  openmpi/3.1.6 python/3.8.8
odule load  gcc/11.2.0 openmpi/4.1.4 python/3.11.1
if ! [ -d "$PROJECT_DIR/ENV3" ]; then
    time python -m venv $PROJECT_DIR/ENV3
fi
source $PROJECT_DIR/ENV3/bin/activate

time pip install pip -U
time pip install -r $EXEC_DIR/requirements-rivanna.txt
which python

end_python_install_time=`date +%s`
echo end_python_install_time $end_python_install_time
time_python_install=$((start_python_install-end_python_install))
echo time_python_install $time_python_install