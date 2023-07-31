#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --time=03:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:v100:2
#SBATCH --job-name=osmi-v100-rivanna
#SBATCH --output=osmi-v100-rivanna-%u-%j.out
#SBATCH --error=osmi-v100-rivanna-%u-%j.err
## SBATCH --mem-per-gpu=48G
#SBATCH --exclusive


NAME=cloudmesh-rivanna
# BASE=/localscratch
# RUN_DIR=$BASE/$USER/osmi
RUN_DIR=$PROJECT/osmi
OUTPUT_DIR="$RUN_DIR/osmi-output"
BENCHMARK_DIR="$RUN_DIR/benchmark"
EXEC_DIR=$RUN_DIR/target/rivanna

REPEAT=0
NUM_HAPROXY_SERVERS=1
NUM_GPUS_PER_NODE=2
# WORKERS=4
HAPROXY_SERVER_BASE=8443
PORT_TF_SERVER_BASE=8500
# PORT_TF_SERVER=$(($PORT_TF_SERVER_BASE + $REPEAT))
CFG_FILE=$BENCHMARK_DIR/haproxy-grpc.cfg
# add new variables
# copy into run-rivanna-v100-project-haproxy-$NUM_NODES-$NUM_GPUS_PER_NODE.slurm

progress() {
    echo "# cloudmesh status=running progress=$1 pid=$$"
}

progress 1
nvidia-smi
hostname
progress 2

progress 3
time mkdir -p $OUTPUT_DIR
progress 4

progress 5
# time cd $RUN_DIR
progress 6
progress 7
progress 8

module purge
module load singularity
# module load  gcc/9.2.0  cuda/11.0.228  openmpi/3.1.6 python/3.8.8
# source $RUN_DIR/ENV3/bin/activate
progress 10

# nextline you comment out initially and next time you run it to see imapct of energy monitoring
# cms gpu watch --gpu=0 --delay=0.5 --dense > $OUTPUT_DIR/v100-gpu.log &

progress 40
# cd $BENCHMARK_DIR

progress 50

echo "# ======= SERVER START"
start_wait_for_server=`date +%s`
echo start_wait_for_server $start_wait_for_server

singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python ModelServer.py --port_tf_server_base=$PORT_TF_SERVER_BASE --num_gpus=$NUM_GPUS_PER_NODE --output_dir=$OUTPUT_DIR --repeat_no=$REPEAT


end_wait_for_server=`date +%s`
echo "server up"
echo end_wait_for_server $end_wait_for_server
time_server_wait=$((end_wait_for_server-start_wait_for_server))
echo time_server_wait $time_server_wait

progress 60

echo "launching load balancer on all nodes"

singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python LoadBalancer.py --port_ha_proxy_base=$HAPROXY_SERVER_BASE --output_dir=$OUTPUT_DIR --exec_dir=$EXEC_DIR --config_file=$CFG_FILE --repeat_no=$REPEAT

echo "# ======= SERVER UP"

progress 90
run_metabench

seff $SLURM_JOB_ID
progress 100