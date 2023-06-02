#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=2-00:00:00
#SBATCH --partition=bii-gpu
#SBATCH --account=bii_dsc_community
#SBATCH --gres=gpu:v100:4
#SBATCH --job-name=osmi-v100-rivanna
#SBATCH --output=osmi-v100-rivanna-%u-%j.out
#SBATCH --error=osmi-v100-rivanna-%u-%j.err
#SBATCH --mem-per-gpu=128G

echo "# cloudmesh status=running progress=1 pid=$$"
nvidia-smi
hostname
echo "# cloudmesh status=running progress=2 pid=$$"

NAME=cloudmesh-rivanna
BASE=/localscratch
RUN_DIR=$BASE/$USER/osmi
EXEC_DIR="$RUN_DIR/machine/rivanna"
OUTPUT_DIR="$RUN_DIR/osmi-output/$SLURM_JOB_ID-output"
BENCHMARK_DIR="$RUN_DIR/benchmark"
PROJECT_DIR=$PROJECT/osmi
HOME_DIR=$PROJECT_DIR/machine/rivanna
# TMP=`pwd`/../..
# PROJECT=`realpath $TMP`
# echo "PROJECT: " $PROJECT
PORT_TF_SERVER=8500


echo "# cloudmesh status=running progress=3 pid=$$"
time mkdir -p $RUN_DIR
time rsync -r $PROJECT_DIR $RUN_DIR/.. --exclude=.git --exclude=Makefile --exclude=ENV3 --exclude=results.ipynb --exclude=*.md --exclude=*.sif --exclude=osmi-output/* --exclude=*.out --exclude=*.err
time mkdir -p $OUTPUT_DIR
echo "# cloudmesh status=running progress=4 pid=$$"

echo "# cloudmesh status=running progress=5 pid=$$"
time cd $RUN_DIR
echo "# cloudmesh status=running progress=6 pid=$$"
ls
du -h $RUN_DIR
echo "# cloudmesh status=running progress=7 pid=$$"
diff $PROJECT_DIR $RUN_DIR/..
echo "# cloudmesh status=running progress=8 pid=$$"

# module load anaconda
# conda activate OSMI
module purge
module load singularity
# module load  gcc/9.2.0  cuda/11.0.228  openmpi/3.1.6 python/3.8.8
# source $PROJECT_DIR/ENV3/bin/activate
# time pip install pip -U
# time pip install -r $EXEC_DIR/requirements-rivanna.txt
echo "# cloudmesh status=running progress=10 pid=$$"

# nextline you comment out initially and next time you run it to see imapct of energy monitoring
# cms gpu watch --gpu=0 --delay=0.5 --dense > $OUTPUT_DIR/v100-gpu.log &

echo "# cloudmesh status=running progress=40 pid=$$"
echo "# ======= SERVER START"
cd $BENCHMARK_DIR
time singularity exec --nv --home `pwd` $HOME_DIR/serving_latest-gpu.sif tensorflow_model_server --port=$PORT_TF_SERVER --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-$PORT_TF_SERVER.log &
echo "# cloudmesh status=running progress=45 pid=$$"

start_wait_for_server=`date +%s`
echo start_wait_for_server $start_wait_for_server

for sec in $(seq -w 10000 -1 1); do
    if [[ $(lsof -i :$PORT_TF_SERVER) ]]; then break; fi
    sleep 0.5
    echo "-"
done

end_wait_for_server=`date +%s`
echo "server up"
echo end_wait_for_server $end_wait_for_server
time_server_wait=$((end_wait_for_server-start_wait_for_server))
echo time_server_wait $time_server_wait

echo "# ======= SERVER UP"
echo "# cloudmesh status=running progress=50 pid=$$"

echo "# cloudmesh status=running progress=60 pid=$$"
echo "# ======= START"
singularity exec --nv --bind /localscratch:/localscratch $HOME_DIR/$NAME.sif \
    python $BENCHMARK_DIR/metabench.py $HOME_DIR/rivanna-V100.yaml \
    -o $OUTPUT_DIR/v100-results-localscratch.csv
singularity exec --nv --bind /localscratch:/localscratch $HOME_DIR/$NAME.sif \
    python $BENCHMARK_DIR/metabench.py $HOME_DIR/fig4-V100-n128.yaml \
    -o $OUTPUT_DIR/v100-results-localscratch-fig4.csv
echo "# ======= END"
echo "# cloudmesh status=running progress=90 pid=$$"

time rsync -r -v $OUTPUT_DIR/* $PROJECT_DIR/osmi-output
ls $OUTPUT_DIR
ls $PROJECT_DIR/osmi-output
rm -r $OUTPUT_DIR

seff $SLURM_JOB_ID
echo "# cloudmesh status=running progress=100 pid=$$"

# echo osmi-v100-rivanna-$USER-$SLURM_JOB_ID.out
# mkdir -p /localscratch/$USER