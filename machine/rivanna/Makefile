run:
	sbatch metabench.slurm

image:
	cd ../../; \
	singularity pull docker://tensorflow/serving:latest-gpu;

clean:
	rm *.err *.out