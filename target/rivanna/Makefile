NAME=osmi

SHELL=/bin/bash
#USER_SCRATCH=/scratch/${USER}
#PROJECT_DIR=${USER_SCRATCH}/mlcommons/benchmarks/${NAME}
#PROJECT_DATA=${USER_SCRATCH}/data
MACHINE=rivanna

.PHONY: images image-docker project

all: requirements data

# #####################################################################
# PROCESS MAAGEMENT
# #####################################################################

process_killer:
	-pkill nvidia-smi
	-pkill cms
	-pkill haproxy

everything: stop process_killer clean project run
	@echo #####################################################################
	@echo "Cool runner is DONE."
	@echo #####################################################################

#TODO
hap:
	# apptainer exec --bind `pwd`:/home --pwd /home ${USER_SCRATCH}/osmi/target/maltlab/images/haproxy_latest.sif haproxy -d -f haproxy-grpc.cfg > ./outputs/haproxy.log 2>&1 &
	# apptainer shell
	apptainer shell ${USER_SCRATCH}/osmi/target/maltlab/images/haproxy_latest.sif


# thats it

# #####################################################################
# REQUIREMENTS
# #####################################################################

requirements:
	time pip install -r ${PROJECT_DIR}/experiments/${MACHINE}/requirements.txt

# #####################################################################
# PROJECT MANAGEMENT
# #####################################################################

project: clean project_json generate

#setup:
#	python setup_env_and_yaml.py
#	source ~/OSMI/bin/activate && pip install -r /scratch/${USER}/mlcommons/benchmarks/${NAME}/experiments/${MACHINE}/requirements.txt

generate: project-jobs.sh

run: submit

submit:
	-sh project-jobs.sh

localscratch: localscratch_json




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
	
# project_json: config.in.yaml
# 	cms ee generate \
# 	           --source=osmi.in.slurm \
# 	           --config=config.in.yaml \
# 	           --name=project \
# 	           --noos \
# 	           --os=USER,HOME \
# 		       --nocm \
# 	           --output_dir=./project \
#              --source_dir=. \
# 		       --verbose \
# 			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
# 	cms ee list

# project-jobs.sh: project.json
# 	cms ee generate submit --name=project  > project-jobs.sh

# project_sh: project.json
# 	cms ee generate \
# 	           --source=osmi.in.sh \
# 	           --config=config.in.yaml \
# 	           --name=project \
# 	           --noos \
# 	           --os=USER,HOME \
# 		       --nocm \
# 	           --output_dir=./project \
#                --source_dir=. \
# 		       --verbose \
# 			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
# 	cms ee generate submit --name=project --job_type=sh > project-jobs-sh.sh
# 	cms ee list
	
project_slurm: 
	cms ee generate \
	           --source=osmi.in.slurm \
	           --config=config.in.yaml \
	           --name=project \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./project \
               --source_dir=. \
		       --verbose \
			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
	cms ee generate submit --name=project --job_type=sbatch > project-jobs-slurm.sh
	cms ee list

project_lsf:
	cms ee generate \
	           --source=osmi.in.lsf \
	           --config=config.in.yaml \
	           --name=project \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./project \
               --source_dir=. \
		       --verbose \
			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
	cms ee generate submit --name=project --job_type=lsf > project-jobs-lsf.sh
	cms ee list

kill: stop

stop:
	-for i in "$$(squeue --user $$USER | awk 'NR>1{print $$1}')"; do scancel $$i ; done

inspect:
	$(eval D=$(shell ls project/$(ls -1) | head -n 1))
	echo ${D}
	$(shell emacs project/${D}/config.yaml project/${D}/job.slurm)

watch: status

status:
	watch squeue --format=\"%.18i %.9P %.50j %.8u %.8T %.10M %.9l %.6D %R\" -u ${USER}

clean:
	@-rm -rf project project.json jobs-project.sh
	@-rm -rf '__pycache__'
	@-rm -rf *~

# PROJECT_USER=/project/bii_dsc_community/tma5gv
PROJECT_USER=/scratch/tma5gv

get-results:
	-rsync -av --progress ${MACHINE}:${PROJECT_USER}/${NAME}/target/${MACHINE}/project .


# #####################################################################
# CLEAN MODELS
# #####################################################################

clean-models:
	cd ../../models; make clean
	
# #####################################################################
# APPTAINER IMAGE BUILD
# #####################################################################

clean-images:
	@-rm -rf images/*.sif

images: image

image: image-osmi image-tfs image-haproxy 

image-haproxy: # images /haproxy_latest.sif
	-cd images; apptainer pull docker://haproxy

image-serving: # images/serving_latest-gpu.sif
	-cd images; apptainer pull docker://tensorflow/serving:latest-gpu

image-osmi: # images/osmi.sif
	-cd images; time apptainer build --force osmi.sif osmi.def

# broken?
image-tfs: # images/tfs.sif
	-cd images; time apptainer build --force tfs.sif tfs.def

# broken?
image-combined: # images/combined.sif
	-cd images; time apptainer build --force combined.sif combined.def


# #####################################################################
# APPTAINER IMAGE SHELL
# #####################################################################

shell:
	apptainer ${BIND} shell --nv ${IMAGE}

shell-serving:
	apptainer ${BIND} shell --nv images/serving.sif

# #####################################################################
# THESE ARE NOT YET DONE AND JUST PLACEHOLDERS
# #####################################################################

# run-osmi:
# 	# cd images; make run


run-apptainer:
	cd images; make run

run-localscratch:
	cd images; make run-localscratch

shell-localscratch:
	cd images; make shell-localscratch

shell-apptainer:
	cd images; make shell

run: run-apptainer

# #####################################################################
# THESE COMMANDS ARE ONLY FOR GREGOR
# #####################################################################

push:
	-git push
	ssh -tt ${MACHINE} "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"

# #####################################################################
# SOME DOCKER TESTING TARGETS. TODO CLEANUP
# #####################################################################

docker-run: build
	docker run -d \
		--name osmi \
		-v "$(realpath $(CURDIR)/../../../):/scratch" \
		--gpus all \
		osmi tail -f /dev/null

build:
	docker build -t osmi .

docker-shell:
	docker exec -it `docker ps -aqf ancestor=osmi | head -n 1` /bin/bash

down:
	@CONTAINERS=$$(docker ps -q -f ancestor=osmi); \
	if [ -n "$$CONTAINERS" ]; then \
		for container in $$CONTAINERS; do \
			echo "Stopping container: $$container"; \
			docker stop $$container; \
			echo "Removing container: $$container"; \
			docker rm $$container; \
		done; \
	else \
		echo "No containers to stop or remove."; \
	fi
	# docker stop `docker ps -aqf ancestor=osmi | head -n 1`
	# docker rm `docker ps -aqf ancestor=osmi | head -n 1`

