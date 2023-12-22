NAME=osmi

SHELL=/bin/bash
#USER_SCRATCH=/scratch/${USER}
#PROJECT_DIR=${USER_SCRATCH}/mlcommons/benchmarks/${NAME}
#PROJECT_DATA=${USER_SCRATCH}/data

.PHONY: image-apptainer image-docker project

all: requirements data

# #####################################################################
# REQUIREMENTS
# #####################################################################

requirements:
	time pip install -r ${PROJECT_DIR}/experiments/rivanna/requirements.txt

# #####################################################################
# PROJECT MANAGEMENT
# #####################################################################

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
	cms ee generate submit --name=$<  > $@

simple:
	cms ee generate \
	           --source=simple.in.slurm \
	           --config=$< \
	           --name=$(basename $@) \
	           --noos \
	           --os=USER,HOME \
		   	   --nocm \
	           --output_dir=./$(basename $@) \
               --source_dir=. \
               --verbose

project.json: config.in.yaml
	cms ee generate \
	           --source=${NAME}.in.slurm \
	           --config=$< \
	           --name=$(basename $@) \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./$(basename $@) \
               --source_dir=. \
		       --verbose \
			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"

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

# PROJECT_USER=/project/bii_dsc_community/tma5gv
PROJECT_USER=/scratch/tma5gv

get-results:
	-rsync -av --progress rivanna:${PROJECT_USER}/${NAME}/target/rivanna/project .

# #####################################################################
# APPTAINER IMAGE BUILD
# #####################################################################

clean-images:
	@-rm -rf image-apptainer/*.sif

images: image

image: image-haproxy image-osmi image-tfs

image-haproxy: # image-apptainer/haproxy_latest.sif
	-cd image-apptainer; time apptainer pull docker://haproxy

image-serving: # image-apptainer/serving_latest-gpu.sif
	-cd image-apptainer; time apptainer pull docker://tensorflow/serving:latest-gpu

image-tfs: # image-apptainer/tfs.sif
	-cd image-apptainer; time apptainer build tfs.sif tfs.def

image-osmi: # image-apptainer/osmi.sif
	-cd image-apptainer; apptainer build osmi.sif osmi.def


# #####################################################################
# APPTAINER IMAGE SHELL
# #####################################################################

shell:
	apptainer ${BIND} shell --nv ${IMAGE}

shell-serving:
	apptainer ${BIND} shell --nv image-apptainer/serving.sif

# #####################################################################
# THESE ARE NOT YET DONE AND JUST PLACEHOLDERS
# #####################################################################

# run-osmi:
# 	# cd image-apptainer; make run


run-apptainer:
	cd image-apptainer; make run

shell-apptainer:
	cd image-apptainer; make shell

run-localscratch:
	cd image-apptainer; make run-localscratch

shell-localscratch:
	cd image-apptainer; make shell-localscratch

shell-rivanna:
	cd image-apptainer; make shell-rivanna

run: run-apptainer

# #####################################################################
# THESE COMMANDS ARE ONLY FOR GREGOR
# #####################################################################

push:
	-git push
	ssh -tt rivanna "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"



