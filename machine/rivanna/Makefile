run:
	sbatch metabench-V100.slurm; \
	sbatch metabench-A100.slurm; \
	sbatch metabench-cpu.slurm;

image:
	cd ../../; \
	singularity pull docker://tensorflow/serving:latest-gpu;

clean:
	rm *.err *.out

squeue:
	squeue -u $$(whoami)