NAME=osmi

SHELL=/bin/bash
#USER_SCRATCH=/scratch/${USER}
#PROJECT_DIR=${USER_SCRATCH}/mlcommons/benchmarks/${NAME}
#PROJECT_DATA=${USER_SCRATCH}/data

.PHONY: image-singularity image-docker project

all: requirements data

image-haproxy:
	mkdir -p image-singularity
	cd image-singularity; time singularity pull docker://haproxy

requirements:
	time pip install -r ${PROJECT_DIR}/experiments/rivanna/requirements.txt

#hallo:
#	echo "HHHHH"
#
#data:
#	# mkdir -p ${PROJECT_DATA}/???
#	echo "ERROR NOT IMPLEMENTED"

project: clean project.json generate

#setup:
#	python setup_env_and_yaml.py
#	source ~/ENV3/bin/activate && pip install -r /scratch/${USER}/mlcommons/benchmarks/${NAME}/experiments/rivanna/requirements.txt

generate: jobs-project.sh 

run: submit

submit:
	-sh jobs-project.sh

localscratch: localscratch.json


jobs-%.sh: %.json
	cms sbatch generate submit --name=$<  > $@


simple:
	cms sbatch generate \
	           --source=simple.in.slurm \
	           --config=$< \
	           --name=$(basename $@) \
	           --noos \
	           --os=USER,HOME \
		   	   --nocm \
	           --output_dir=./$(basename $@) \
               --source_dir=. \
               --verbose


%.json: config.in.yaml
	cms sbatch generate \
	           --source=${NAME}.in.slurm \
	           --config=$< \
	           --name=$(basename $@) \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./$(basename $@) \
               --source_dir=. \
		       --verbose \
			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,simple_osmi.py,osmi-bench.py,haproxy-grpc.cfg"

kill: stop

stop:
	for i in "$$(squeue --user $$USER | awk 'NR>1{print $$1}')"; do scancel $$i ; done

inspect:
	$(eval D=$(shell ls project/$(ls -1) | head -n 1))
	echo ${D}
	$(shell emacs project/${D}/config.yaml project/${D}/job.slurm)

watch: status

status:
	watch squeue --format=\"%.18i %.9P %.50j %.8u %.8T %.10M %.9l %.6D %R\" --me


clean:
	@-rm -rf project project.json jobs-project.sh
	@-rm -rf '__pycache__'
	@-rm -rf *~

clean-images:
	@-rm -rf image-singularity/*.sif


# run-osmi:
# 	# cd image-singularity; make run


image-tfs:
	cd image-singularity; time singularity pull docker://tensorflow/serving:latest-gpu

image-osmi:
	cd image-singularity; cms rivanna singularity build ${NAME}.def

shell:
	singularity ${BIND} shell --nv ${IMAGE}

run-singularity:
	cd image-singularity; make run

shell-singularity:
	cd image-singularity; make shell

run-localscratch:
	cd image-singularity; make run-localscratch

shell-localscratch:
	cd image-singularity; make shell-localscratch

shell-rivanna:
	cd image-singularity; make shell-rivanna

run: run-singularity

image: image-haproxy image-osmi image-tfs

push:
	-git push
	ssh -tt rivanna "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"


shell: shell-singularity
