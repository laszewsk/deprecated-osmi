#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:a100
#SBATCH --job-name=train-osmi
#SBATCH --output=%u-%j.out
#SBATCH --error=%u-%j.err
#SBATCH --reservation=bi_fox_dgx
#SBATCH --constraint=a100_80gb
#SBATCH --mem-per-gpu=16G

## SBATCH -c 4
## SBATCH --mem=16GB

echo "# cloudmesh status=running progress=1 pid=$$"
nvidia-smi
echo "# cloudmesh status=running progress=2 pid=$$"

export BASE=/scratch
export RUN_DIR=$BASE/$USER/osmi
output_dir="$RUN_DIR/osmi-output"
benchmark="$RUN_DIR/benchmark"
rivanna="$RUN_DIR/machine/rivanna"
TMP=`pwd`/../..
export PROJECT=`realpath $TMP`
echo "PROJECT: " $PROJECT
export SRC_DIR=$PROJECT


echo "# cloudmesh status=running progress=3 pid=$$"
time mkdir -p $RUN_DIR
time rsync -r -v $PROJECT $RUN_DIR/.. --exclude=.git
echo "# cloudmesh status=running progress=4 pid=$$"

echo "# cloudmesh status=running progress=5 pid=$$"
time cd $RUN_DIR
echo "# cloudmesh status=running progress=6 pid=$$"
ls
du -h $RUN_DIR
echo "# cloudmesh status=running progress=7 pid=$$"
diff $PROJECT $RUN_DIR/..
echo "# cloudmesh status=running progress=8 pid=$$"

module load anaconda
conda activate OSMI
time pip install --user -r $rivanna/requirements-rivanna.txt
echo "# cloudmesh status=running progress=10 pid=$$"

# nextline you comment out initially and next time you run it to see imapct of energy monitoring
# cms gpu watch --gpu=0 --delay=0.5 --dense > outputs/gpu0.log &

echo "# cloudmesh status=running progress=40 pid=$$"
echo "# ======= SERVER START"
cd $benchmark
time singularity run --nv --home `pwd` $RUN_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& $output_dir/log &
echo "# cloudmesh status=running progress=45 pid=$$"

start_wait_for_server=`date +%s`
echo start_wait_for_server $start_wait_for_server
# for sec in $(seq -w 10000 -1 1); do
#     if [[ $(lsof -i :8500) ]]; then break; fi
#     sleep 0.5
#     echo "-"
# done
sleep 4
lsof -i :8500
time python $rivanna/test-socket.py 8500
end_wait_for_server=`date +%s`
echo "server up"
echo end_wait_for_server $end_wait_for_server
time_server_wait=$((start_wait_for_server-end_wait_for_server))
echo time_server_wait $time_server_wait

echo "# ======= SERVER UP"
echo "# cloudmesh status=running progress=50 pid=$$"


echo "# cloudmesh status=running progress=60 pid=$$"
echo "# ======= START"
time python metabench.py $rivanna/rivanna-A100.yaml -o $output_dir/a100-results-scratch.csv
echo "# ======= END"
echo "# cloudmesh status=running progress=90 pid=$$"

time rsync -r -v $output_dir $PROJECT/osmi-output

seff $SLURM_JOB_ID
echo "# cloudmesh status=running progress=100 pid=$$"
