#!/bin/bash

# Job name
#SBATCH -J start_services

# Output and error files
#SBATCH -o start_services.out
#SBATCH -e start_services.err

#
# add other directives
#

# Request resources
#SBATCH -n 3
#SBATCH --time=00:10:00

# Load Singularity module
module load singularity

#
# haproxy.cfg needs to be in cwd, cange the 
#
# Start HAProxy
singularity exec  haproxy.sif /bin/bash -c 'python3 /path/to/haproxy_manager.py start ./haproxy.cfg' &

# Start TFS and wait for HAProxy
singularity exec --bind /etc/haproxy:/etc/haproxy tfs_haproxy.sif /bin/bash -c 'python3 /path/to/tfs_start_script.py' &

# Poll HAProxy and TFS status until both are up and running
HA_PROXY_UP=0
TFS_UP=0

#
# use proper name of haproxy_manager
#
while [[ $HA_PROXY_UP -ne 1 ]] || [[ $TFS_UP -ne 1 ]]; do
    singularity exec --bind /etc/haproxy:/etc/haproxy haproxy.sif /bin/bash -c 'python3 ./cloudmesh-osmi/haproxy_manager.py status'
    HA_PROXY_UP=$?

    singularity exec --bind /etc/haproxy:/etc/haproxy tfs_haproxy.sif /bin/bash -c 'python3 /path/to/tfs_status_script.py'
    TFS_UP=$?

    sleep 5
done

# Start the program osmi
/path/to/osmi_prg
