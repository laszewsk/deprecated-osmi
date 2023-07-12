#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:v100:2
#SBATCH --job-name=osmi-v100-rivanna
#SBATCH --output=osmi-v100-rivanna-%u-%j.out
#SBATCH --error=osmi-v100-rivanna-%u-%j.err
#SBATCH --mem-per-gpu=128G


# https://www.rc.virginia.edu/userinfo/rivanna/software/engineering/
# https://stackoverflow.com/questions/61896426/slurm-srun-run-a-python-script-not-in-parallel-but-have-access-to-the-parallel
# srun python myscript.py
# Wes Brewer8:19 PM
# https://code.ornl.gov/whb/osmi-bench/-/tree/main/benchmark
# Wes Brewer8:23 PM
# srun -n 4 singularity exec --bind `pwd`:/home --pwd /home haproxy_latest.sif haproxy -d -f $CFG_FILE >& $WORKDIR/haproxy.log &

echo "# cloudmesh status=running progress=1 pid=$$"
nvidia-smi
hostname
echo "# cloudmesh status=running progress=2 pid=$$"

NAME=cloudmesh-rivanna
# BASE=/localscratch
# RUN_DIR=$BASE/$USER/osmi
# EXEC_DIR="$RUN_DIR/machine/rivanna"
RUN_DIR=$PROJECT/osmi
OUTPUT_DIR="$RUN_DIR/osmi-output"
BENCHMARK_DIR="$RUN_DIR/benchmark"
EXEC_DIR=$RUN_DIR/machine/rivanna
PORT_TF_SERVER=8500

REPEAT=0
NUM_HAPROXY_SERVERS=1
NUM_GPUS_PER_NODE=2
NUM_OF_NODES=1
# WORKERS=4
PORT_TF_SERVER_BASE=8500
PORT_TF_SERVER=$(($PORT_TF_SERVER_BASE + $REPEAT))
# add new variables
# copy into run-rivanna-v100-project-haproxy-$NUM_NODES-$NUM_GPUS_PER_NODE.slurm
echo "# cloudmesh status=running progress=3 pid=$$"
time mkdir -p $OUTPUT_DIR
echo "# cloudmesh status=running progress=4 pid=$$"

echo "# cloudmesh status=running progress=5 pid=$$"
time cd $RUN_DIR
echo "# cloudmesh status=running progress=6 pid=$$"
echo "# cloudmesh status=running progress=7 pid=$$"
echo "# cloudmesh status=running progress=8 pid=$$"

module purge
module load singularity
# module load  gcc/9.2.0  cuda/11.0.228  openmpi/3.1.6 python/3.8.8
# source $RUN_DIR/ENV3/bin/activate
echo "# cloudmesh status=running progress=10 pid=$$"

# nextline you comment out initially and next time you run it to see imapct of energy monitoring
# cms gpu watch --gpu=0 --delay=0.5 --dense > $OUTPUT_DIR/v100-gpu.log &

echo "# cloudmesh status=running progress=40 pid=$$"
echo "# ======= SERVER START"
cd $BENCHMARK_DIR

for gpu in `seq 0 $(($NUM_GPUS_PER_NODE-1))`
do
    PORT=$(($PORT_TF_SERVER+$j))
    time CUDA_VISIBLE_DEVICES=$gpu singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=$PORT --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-$PORT.log &
done

# time CUDA_VISIBLE_DEVICES=1 singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8501 --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-8501.log &
echo "# cloudmesh status=running progress=45 pid=$$"
start_wait_for_server=`date +%s`
echo start_wait_for_server $start_wait_for_server

# for sec in $(seq -w 10000 -1 1); do
#     if [[ $(lsof -i :8500) && $(lsof -i :8501) ]]; then break; fi
#     sleep 0.5
#     echo "-"
# done
for sec in $(seq -w 10000 -1 1); do
    valid=1
    for PORT in `seq $PORT_TF_SERVER $(($PORT_TF_SERVER+$NUM_GPUS_PER_NODE-1))`; do
        if ! [[ $(lsof -i :$PORT) ]]; then
            valid=0;
            break;
        fi
    done
    if [ $valid = 1 ]; then break; fi;
    sleep 0.5
    echo "-"
done

end_wait_for_server=`date +%s`
echo "server up"
echo end_wait_for_server $end_wait_for_server
time_server_wait=$((end_wait_for_server-start_wait_for_server))
echo time_server_wait $time_server_wait

echo "# cloudmesh status=running progress=50 pid=$$"

CFG_FILE=$BENCHMARK_DIR/haproxy-grpc.cfg
echo "launching load balancer on all nodes"
time singularity exec --bind `pwd`:/home --pwd /home \
    $EXEC_DIR/haproxy_latest.sif haproxy -d -f $CFG_FILE >& $BENCHMARK_DIR/haproxy.log &
echo checking port 8443 to see if HAProxy is running...
for sec in $(seq -w 10000 -1 1); do
    if [[ $(lsof -i :8443) ]]; then break; fi
    sleep 0.5
    echo "-"
done
lsof -i :8443

echo "# ======= SERVER UP"

echo "# cloudmesh status=running progress=60 pid=$$"

echo "# ======= START"
singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python $BENCHMARK_DIR/metabench.py $EXEC_DIR/rivanna-V100.yaml \
    -o $OUTPUT_DIR/v100-results-localscratch-c2.csv
singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python $BENCHMARK_DIR/metabench.py $EXEC_DIR/fig4-V100-n128.yaml \
    -o $OUTPUT_DIR/v100-results-localscratch-fig4-c2.csv
echo "# ======= END"

echo "# cloudmesh status=running progress=90 pid=$$"

seff $SLURM_JOB_ID
echo "# cloudmesh status=running progress=100 pid=$$"
