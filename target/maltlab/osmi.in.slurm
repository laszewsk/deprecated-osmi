#!/usr/bin/env bash

#SBATCH --job-name=o-m-{experiment.model}-b-{experiment.batch}-n-{experiment.ngpus}-g-{experiment.card_name}-c-{experiment.concurrency}-{experiment.repeat}
#SBATCH --output=osmi-{experiment.repeat}-%u-%j.out
#SBATCH --error=osmi-{experiment.repeat}-%u-%j.err
{slurm.sbatch}
#SBATCH --nodes={ee.nodes}
#SBATCH --ntasks={ee.ntasks}
#SBATCH --mem={ee.mem}
#SBATCH --gres=gpu:{experiment.card_name}:{experiment.ngpus}
#SBATCH --cpus-per-task=1
#SBATCH --time={ee.time}
#SBATCH --exclusive

# slurm.sbatch
# #SBATCH --gres=gpu:a100:1
# #SBATCH --mem-per-gpu={ee.mem_per_gpu}


PROGRESS () {
    echo "# ###########################################"
    echo "# cloudmesh status="$1" progress=$2 pid=$$"
    echo "# ###########################################"
}

PROGRESS "running" 1

echo "# ==================================="
echo "# SLURM info"
echo "# ==================================="

echo USER {os.USER}
echo HOME {os.HOME}
echo cardname {experiment.card_name}
echo ngpus {experiment.ngpus}
echo repeat {experiment.repeat}
echo jobno $SLURM_JOB_ID
echo {slurm.ee}
echo mem {ee.mem}
echo USER $USER
echo {data.sif_dir}

PROGRESS "running" 2

echo "# ==================================="
echo "# PROJECT info"
echo "# ==================================="

USER_PROJECT={project.user}
CONFIG_FILE=config.yaml
TFS_SIF={data.tfs_sif}
HAPROXY_SIF={data.haproxy_sif}
OSMI_SIF={data.osmi_sif}
OUTPUT_DIR={data.output}

echo USER_PROJECT $USER_PROJECT
echo CONFIG_FILE $CONFIG_FILE
echo TFS_SIF $TFS_SIF
echo HAPROXY_SIF $HAPROXY_SIF
echo OSMI_SIF $OSMI_SIF
echo CLOUDMESH_CONFIG_DIR $CLOUDMESH_CONFIG_DIR
echo OUTPUT_DIR $OUTPUT_DIR

mkdir -p $OUTPUT_DIR

mkdir -p $USER

PROGRESS "running" 3

head /proc/meminfo

# module purge
# module load apptainer gcc/11.2.0 openmpi/4.1.4 python/3.11.1

source $BASE/ENV3/bin/activate

for gpu in $(seq 0 {experiment.ngpus}); do
    cms gpu watch --gpu=$gpu --delay=0.5 --dense > $OUTPUT_DIR/gpu-0.log &
done

python ModelServer.py start_and_wait --config=$CONFIG_FILE

python LoadBalancer.py start_and_wait --config=$CONFIG_FILE

python Client.py run --config=$CONFIG_FILE

nvidia-smi

# python ModelServer.py start --config=$CONFIG_FILE &

# python LoadBalancer.py start --config=$CONFIG_FILE &

# python ModelServer.py wait --config=$CONFIG_FILE

# python LoadBalancer.py wait --config=$CONFIG_FILE

# time python Client.py --config=$CONFIG_FILE
