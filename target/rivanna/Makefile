NAME=cloudmesh
BUILD=${NAME}.def
IMAGE=${NAME}.sif

images: image image-nvidia

image-docker: ${NAME}-rivanna.def ${NAME}-rivanna.sif
	cp ${NAME}-rivanna.def build.def
	sudo /opt/singularity/3.7.1/bin/singularity build output_image.sif build.def
	cp output_image.sif ${NAME}-rivanna.sif
	make -f Makefile clean

image-nvidia: ${NAME}-nvidia.def ${NAME}-nvidia.sif
	cp ${NAME}-nvidia.def build.def
	sudo /opt/singularity/3.7.1/bin/singularity build output_image.sif build.def
	cp output_image.sif ${NAME}-nvidia.sif
	make -f Makefile clean

clean:
	rm -rf build.def output_image.sif

clear:
	rm -f *.err *.out

queue: watch

watch: status

status:
	watch squeue --format=\"%.18i %.9P %.50j %.8u %.8T %.10M %.9l %.6D %R\" --me

delete: 
	rm -f *.out *.err

ijob:
#	ijob -c 1 -A bii_dsc_community -p bii-gpu --reservation=bi_fox_dgx --gres=gpu:a100:1 --time=0-00:10:00
	ijob -c 1 -A bii_dsc_community -p bii-gpu --gres=gpu:v100:1 --time=0-00:10:00
	#ijob -c 1 -A comp4gc -p bii-gpu --gres=gpu:v100:1 --time=0-00:10:00

shell:
	singularity shell mnist.sif

view:
	watch tail *.out

all: delete clean image run-a100 watch

all-gpu:
	make -f Makefile run-v100
	make -f Makefile run-k80
	make -f Makefile run-p100
	make -f Makefile run-rtx3090

run:
	sbatch run-localscratch-v100.slurm; \
	sbatch run-localscratch-a100.slurm; \
	sbatch run-localscratch-cpu.slurm

environment:
	sbatch environment.slurm

tf-image:
	singularity pull docker://tensorflow/serving:latest-gpu

train:
	sbatch train.slurm

squeue:
	squeue -u $$USER

scancel:
	scancel -u $$USER