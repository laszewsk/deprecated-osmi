#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii-gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --account=bii_dsc_community
#SBATCH --job-name=python3-setup
#SBATCH --output=environment-%u-%j.out
#SBATCH --error=environment-%u-%j.err
#SBATCH --mem-per-gpu=64G

if [ -z "$BASE" ]; then
    echo "BASE is not set"
    exit 1
fi

start_python_install=`date +%s`
echo start_python_install $start_python_install

module purge
module load gcc/11.4.0  openmpi/4.1.4 python/3.11.4
if ! [ -d "$BASE/ENV3" ]; then
    time python -m venv $BASE/ENV3
fi
source $BASE/ENV3/bin/activate

time pip install pip -U
time pip install -r $EXEC_DIR/requirements-baremetal.txt
which python
python --version
cms help

end_python_install_time=`date +%s`
echo end_python_install_time $end_python_install_time
time_python_install=$((end_python_install-start_python_install))
echo time_python_install $time_python_install



