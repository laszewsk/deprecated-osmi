#!/usr/bin/env bash

#SBATCH --job-name=o-m-{experiment.model}-b-{experiment.batch}-n-{experiment.ngpus}-g-{experiment.card_name}-c-{experiment.concurrency}-{experiment.repeat}
#SBATCH --output=osmi-{experiment.repeat}-%u-%j.out
#SBATCH --error=osmi-{experiment.repeat}-%u-%j.err
{slurm.ee}
#SBATCH --nodes={ee.nodes}
#SBATCH --ntasks={ee.ntasks}
#SBATCH --mem={ee.mem}
#SBATCH --gres=gpu:{experiment.card_name}:{experiment.ngpus}
#SBATCH --cpus-per-task=1
#SBATCH --time={ee.time}


# xSBATCH --partition=gpu
# xSBATCH --mem=64GB


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

# WORKDIR=$USER_PROJECT/osmi
# SIF_DIR=$WORKDIR/target/rivanna/image-singularity
USER_PROJECT=/project/bii_dsc_community/$USER
CONFIG_FILE=config.yaml
TFS_SIF={data.tfs_sif}
HAPROXY_SIF={data.haproxy_sif}
OSMI_SIF={data.osmi_sif}

# echo NAME $NAME
# echo WORKDIR $WORKDIR
# echo SIF_DIR $SIF_DIR
echo USER_PROJECT $USER_PROJECT
echo CONFIG_FILE $CONFIG_FILE
echo TFS_SIF $TFS_SIF
echo HAPROXY_SIF $HAPROXY_SIF
echo OSMI_SIF $OSMI_SIF

mkdir -p {data.output}

PROGRESS "running" 3

module purge
module load singularity gcc/11.2.0 openmpi/4.1.4 python/3.11.1

source $USER_PROJECT/ENV3/bin/activate

python ModelServer.py --config=$CONFIG_FILE

python LoadBalancer.py --config=$CONFIG_FILE

python simple_osmi.py --config=$CONFIG_FILE


# singularity exec --nv --bind /localscratch:/localscratch $TFS_SIF \
#     python3 ModelServer.py --config=$CONFIG_FILE

# singularity exec --nv --bind /localscratch:/localscratch $HAPROXY_SIF \
#     python3 LoadBalancer.py --config=$CONFIG_FILE

# singularity exec --nv --bind /localscratch:/localscratch $OSMI_SIF \
#     python simple_osmi.py --config=$CONFIG_FILE



# start osmi bench program with correct number of instanciations (concurrency) through command line
# singularity exec??
# shutdown model server
# shutdown haproxy



#     # python ModelServer.py --port=$PORT_TF_SERVER_BASE --num_gpus=$NUM_GPUS_PER_NODE --output_dir=$OUTPUT_DIR

# PROGRESS "running" 2
#     # python LoadBalancer.py -p 8443 -o ../../osmi-output/ -c haproxy-grpc.cfg

# PROGRESS "running" 3

