NAME=osmi

SHELL=/bin/bash

OS_TYPE=macos
OS_DIR=..
PROJECT_DIR=../..

.PHONY: image-apptainer image-docker project

benchmark:
	-make project
	-make run  

all: requirements data

# #####################################################################
# REQUIREMENTS
# #####################################################################

requirements:
	time pip install -r ../requirements.txt -U

# #####################################################################
# PROJECT MANAGEMENT
# #####################################################################

project: project_slurm generate

#setup:
#	python setup_env_and_yaml.py
#	source ~/ENV3/bin/activate && pip install -r /scratch/${USER}/mlcommons/benchmarks/${NAME}/experiments/rivanna/requirements.txt

generate: project-jobs-slurm.sh

run: submit

submit:
	-sh project-jobs-slurm.sh

project_slurm:
	cms ee generate \
	        --source=model.in.slurm \
	        --config=config.in.yaml \
	        --name=project \
	        --noos \
	        --os=USER,HOME \
		   	--nocm \
	        --output_dir=./project \
            --source_dir=. \
		   --verbose 
			   # \
			   # --copycode="models.py"
	cms ee generate submit --name=project --job_type=slurm > project-jobs-slurm.sh
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

shell-rivanna:
	cd image-apptainer; make shell-rivanna

run: run-apptainer

# #####################################################################
# THESE COMMANDS ARE ONLY FOR GREGOR
# #####################################################################

push:
	-git push
	ssh -tt rivanna "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"



