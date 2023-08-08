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
PORT_TF_SERVER=8500

REPEAT=0
NUM_HAPROXY_SERVERS=1
NUM_GPUS_PER_NODE=2
NUM_OF_NODES=1
# WORKERS=4
PORT_TF_SERVER_BASE=8500
PORT_TF_SERVER=$(($PORT_TF_SERVER_BASE + $REPEAT))
CFG_FILE=$BENCHMARK_DIR/haproxy-grpc.cfg
# add new variables
# copy into run-rivanna-v100-project-haproxy-$NUM_NODES-$NUM_GPUS_PER_NODE.slurm


start_tf_servers() {
    for j in `seq 0 $(($NUM_GPUS_PER_NODE-1))`
    do
        PORT=$(($PORT_TF_SERVER+$j))
        time CUDA_VISIBLE_DEVICES=$j singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=$PORT --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-$PORT.log &
    done

    # time CUDA_VISIBLE_DEVICES=1 singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8501 --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-8501.log &
    # time CUDA_VISIBLE_DEVICES=0 singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-8500.log &
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
}

start_load_balancer() {
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
}

run_metabench() {
    echo "# ======= START"
    singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
        python $BENCHMARK_DIR/metabench.py $EXEC_DIR/rivanna-V100.yaml \
        -o $OUTPUT_DIR/v100-results-localscratch-c2.csv
    singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
        python $BENCHMARK_DIR/metabench.py $EXEC_DIR/fig4-V100-n128.yaml \
        -o $OUTPUT_DIR/v100-results-localscratch-fig4-c2.csv
    echo "# ======= END"
}

run_benchmark() {
    echo "# cloudmesh status=running progress=50 pid=$$"
    # start_tf_servers
    python ModelServer.py --port=$PORT_TF_SERVER_BASE --num_gpus=$NUM_GPUS_PER_NODE
    echo "# cloudmesh status=running progress=60 pid=$$"
    start_load_balancer
    echo "# cloudmesh status=running progress=90 pid=$$"
    run_metabench
}

echo "# cloudmesh status=running progress=1 pid=$$"
nvidia-smi
hostname
echo "# cloudmesh status=running progress=2 pid=$$"

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

echo "# cloudmesh status=running progress=50 pid=$$"
singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python ModelServer.py --port=$PORT_TF_SERVER_BASE --num_gpus=$NUM_GPUS_PER_NODE --output_dir=$OUTPUT_DIR

singularity exec --nv --bind /localscratch:/localscratch $EXEC_DIR/$NAME.sif \
    python LoadBalancer.py -p 8443 -o ../../osmi-output/ -c haproxy-grpc.cfg
echo "# cloudmesh status=running progress=60 pid=$$"
# start_load_balancer
echo "# cloudmesh status=running progress=90 pid=$$"
run_metabench

seff $SLURM_JOB_ID
echo "# cloudmesh status=running progress=100 pid=$$"