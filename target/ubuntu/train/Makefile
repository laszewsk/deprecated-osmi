NAME=osmi

SHELL=/bin/bash

OS_TYPE=ubuntu
OS_DIR=..
PROJECT_DIR=../..

.PHONY: image-apptainer image-docker project

benchmark:
	-make clean
	-make project
	-make run  

all: requirements data

test: clean project_sh generate submit
	cat project/*/*.out

# #####################################################################
# REQUIREMENTS
# #####################################################################

requirements:
	time pip install -r ../requirements.txt -U

# #####################################################################
# PROJECT MANAGEMENT
# #####################################################################

project: project_sh generate

#setup:
#	python setup_env_and_yaml.py
#	source ~/ENV3/bin/activate && pip install -r /scratch/${USER}/mlcommons/benchmarks/${NAME}/experiments/rivanna/requirements.txt

generate: project-jobs-sh.sh

run: submit

submit:
	-sh project-jobs-sh.sh
	
project_sh:
	cms ee generate \
	           --source=model.in.sh \
	           --config=config.in.yaml \
	           --name=project \
	           --noos \
	           --os=USER,HOME \
		       --nocm \
	           --output_dir=./project \
               --source_dir=. \
		       --verbose \
			   --copycode="../../../models"
	cms ee generate submit --name=project --job_type=sh > project-jobs-sh.sh
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

WORKDIR := $(shell pwd)


docker-image:
	cd ../image-docker/train; docker build -t "osmi_train:latest" .



image-osmi: docker image

docker-shell:
	docker run -it --gpus=all --mount type=bind,source=${WORKDIR}/project,target=/workspace/project osmi_train bash

# #####################################################################
# THESE COMMANDS ARE ONLY FOR GREGOR
# #####################################################################

push:
	-git push
	ssh -tt rivanna "cd /scratch/thf2bn/mlcommons/benchmarks/${NAME}; ssh-add; git pull"



