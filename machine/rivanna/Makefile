run:
	sbatch run-localscratch-v100.slurm; \
	sbatch run-localscratch-a100.slurm; \
	sbatch run-localscratch-cpu.slurm

environment:
	sbatch environment.slurm

image:
	singularity pull docker://tensorflow/serving:latest-gpu

train:
	sbatch train.slurm

clean:
	rm *.err *.out

squeue:
	squeue -u $$USER

scancel:
	scancel -u $$USER
