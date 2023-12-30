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
	time pip install -r ${PROJECT_DIR}/experiments/maltlab/requirements.txt

# #####################################################################
# PROJECT MANAGEMENT
# #####################################################################

project: clean project_json generate

#setup:
#	python setup_env_and_yaml.py
#	source ~/ENV3/bin/activate && pip install -r /scratch/${USER}/mlcommons/benchmarks/${NAME}/experiments/maltlab/requirements.txt

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
	
# project.json: config.in.yaml
# 	cms ee generate \
# 	           --source=osmi.in.slurm \
# 	           --config=config.in.yaml \
# 	           --name=project \
# 	           --noos \
# 	           --os=USER,HOME \
# 		       --nocm \
# 	           --output_dir=./project \
#                --source_dir=. \
# 		       --verbose \
# 			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
# 	cms ee list

# project-jobs.sh: project.json
# 	cms ee generate submit --name=project  > project-jobs.sh

project_sh: project.json
	cms ee generate \
	           --source=osmi.in.sh \
	           --config=config.in.yaml \
	           --name=project \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./project \
               --source_dir=. \
		       --verbose \
			   --copycode="benchmark.py,haproxy-grpc.cfg,tfs_grpc_client.py,models.py,smi.py,LoadBalancer.py,ModelServer.py,yaml_to_conf.py,Client.py,osmi-bench.py,haproxy_cfg_generator.py,port_generator.py"
	cms ee generate submit --name=project --job_type=sh > project-jobs-sh.sh
	cms ee list
	
project_slurm: project.json
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

project_lsf: project.json
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
	-rsync -av --progress maltlab:${PROJECT_USER}/${NAME}/target/maltlab/project .

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


image-osmi: # image-apptainer/osmi.sif
	-cd image-apptainer; apptainer build osmi.sif osmi.def

# broken?
image-tfs: # image-apptainer/tfs.sif
	-cd image-apptainer; time apptainer build tfs.sif tfs.def

# broken?
image-combined: # image-apptainer/combined.sif
	-cd image-apptainer; apptainer build combined.sif combined.def


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

shell-maltlab:
	cd image-apptainer; make shell-maltlab

run: run-apptainer

# #####################################################################
# THESE COMMANDS ARE ONLY FOR GREGOR
# #####################################################################

push:
	-git push
	ssh -tt maltlab "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"



