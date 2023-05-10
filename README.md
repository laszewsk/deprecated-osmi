# mlcommons-osmi

Authors: Nate Kimball, Gregor von Laszewski

## Table of contents

1. [Running OSMI Bench on a local Windows machine running WSL](#running-osmi-bench-on-a-local-windows-wsl)

2. [Running OSMI Bench on a local machine running Ubuntu](#running-osmi-bench-on-ubuntu)
   1. [Create python virtual environment](#create-python-virtual-environment-on-ubuntu)
   2. [Get the code](#get-the-code)
   3. [Running the small OSMI model benchmark](#running-the-small-osmi-model-benchmark)
   4. [Install tensorflow serving in ubuntu](#install-tensorflow-serving-in-ubuntu)


3. [Running OSMI Bench on Rivanna](#running-osmi-bench-on-rivanna)
   1. [Get the code](#set-up-a-project-directory-and-get-the-code)
   2. [Set up Python Environment](#set-up-python-environment)
   3. [Get Tensorflow Serving](#pull-tensorflow-serving-image)
   4. [Running the small OSMI model benchmark](#compile-osmi-models-in-interactive-jobs)
   5. [Running test sweep](#run-test-sweep-via-batch-jobs)
   6. [Graph Results](#graphing-results)

## Running OSMI Bench on a local Windows WSL

TODO: Nate

1. create isolated new wsl environment
2. use what we do in the ubuntu thing, but do separate documentation er as the ubuntu native install may have other steps or issuse


### Create python virtual environment on WSL Ubuntu

```
wsl> python3 -m venv /home/$USER/OSMI
wsl> source /home/$USER/OSMI/bin/activate
wsl> python -V
wsl> pip install pip -U
```

### Get the code

To get the [code](<https://code.ornl.gov/whb/osmi-bench>) we clone a gitlab instance that is hosted at Oakridge National Laboratory , please execute:

```
export PROJECT=/home/$USER/project/osmi
mkdir -p $PROJECT
cd $PROJECT
git clone https://github.com/DSC-SPIDAL/mlcommons-osmi.git
git clone https://code.ornl.gov/whb/osmi-bench.git
cd osmi-bench
pip install -r $PROJECT/mlcommons-osmi/wsl/requirements.txt
```

###

```
wsl> cd $PROJECT/mlcommons-osmi/wsl
wsl> 
wsl> make image
wsl> cd models
wsl> time python train.py small_lstm (14.01s user 1.71s system 135% cpu 11.605 total)
wsl> time python train.py medium_cnn (109.20s user 6.84s system 407% cpu 28.481 total)
wsl> time python train.py large_tcnn
cd .. 
```

## Running OSMI Bench on Ubuntu

### Create python virtual environment on Ubuntu

TODO: Gregor
```
python -m venv ~/OSMI
source ~/OSMI/bin/activate
pip install pip -U
```

### Get the code

To get the code we clone this github repository (https://github.com/laszewsk/osmi.git). Please execute:

```
mkdir ~/osmi
cd ~/osmi
git clone https://github.com/laszewsk/osmi.git
cd osmi
pip install -r ~/osmi/osmi/machine/ubuntu/requirements-ubuntu.txt
```

**Note: the original version of grpcio 1.0.0 does not distribute valid wheels, hence we assume the library is out of date, but a new version with 1.15.1 is available that is distributed. Gregor strongly recoomnds to swithc to a supported version of grpcio.**

### Running the small OSMI model benchmark

```
cd models
time python train.py small_lstm  # taks about 10s on an 5950X
time python train.py medium_cnn  # taks less the 12s on an 5950X
time python train.py large_tcnn  # takes less the 30s on an 5950X
```

### Install tensorflow serving in ubuntu

Unclear. the documentation do this with singularity, I do have singularity on desktop, but can we use it natively and compare with singularity performance?

Nate will explore theoretically how to isntall tensorflow servving on ubuntu

compare if others have install instructions, these are old from 16.01 but we want 21. ...

```
sudo pip install tensorflow-serving-api
echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install tensorflow-model-server
which tensorflow_model_server
make image
```

### Running the program

```
cd ~/osmi/osmi/machine/ubuntu
make run
python metabench.py --config=make-yaml-file-for-ubuntu
```
TODO: complete

## Running OSMI Bench on rivanna

To run the OSMI benchmark, you will first need to generate the project directory with the code. We assume you are in the group `bii_dsc_community`. This allows you access to the directory

```/project/bii_dsc_community```

As well as the slurm partitions `gpu` and `bii_gpu`

### Set up a project directory and get the code

<!-- To get the code we clone a gitlab instance that is hosted at Oakridge National Laboratory (<https://code.ornl.gov/whb/osmi-bench>). -->
To get the code we clone this github repository (https://github.com/laszewsk/osmi.git)  First you need to create a directory under your username in the project directory. We recommend to use your username. Follow these steps: 

```
export USER_SCRATCH=/scratch/$USER
export USER_LOCALSCRATCH=/localscratch/$USER
export USER_PROJECT=/project/bii_dsc_community/$USER
export BASE=$USER_PROJECT
```
You can have the project in either USER_PROJECT or USER_SCRATCH
```
export PROJECT=$BASE
```

```
mkdir -p $PROJECT
cd $PROJECT
git clone https://github.com/laszewsk/osmi.git
cd osmi
export EXEC_DIR=$PROJECT/osmi/machine/rivanna
```

### Set up Python Environment

```
rivanna> cd $EXEC_DIR
rivanna> make environment
(this may take a while to finish due to rivanna's slow file system)
rivanna> source ../../ENV3/bin/activate
```

### Interacting with Rivanna

Rivanna has two brimary modes so users can interact with it. 

* **Interactive Jobs:** The first one are interactive jobs that allow you to 
  reserve a node on rivanna so it looks like a login node. This interactive mode is
  usefull only during the debug phase and can serve as a convenient way to quickly create 
  batch scripts that are run in the second mode.

*  **Batch Jobs:** The second mode is a batch job that is controlled by a batch script. 
   We will showcase here how to set such scripts up and use them 


### Pull Tensorflow Serving Image

```
rivanna> cd $EXEC_DIR
rivanna> make image
```

### Compile OSMI Models in Interactive Jobs

Once you know hwo to create jobs with a propper batch script you will likely no longer need to use interactive jobs. We keep this documentation for beginners that like to experiement in interactive mode to develop batch scripts.

First, obtain an interactive job with

```
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=01:00:00
```

*note: use --partition=bii-gpu --gres=gpu:v100:n to recieve n v100 GPUs

```
node> cd $PROJECT/osmi
node> make train
```

For this application there is no separate data

### Compile OSMI Models in Batch Jobs

```
rivanna> cd $EXEC_DIR
rivanna> make train
```

### Run test sweep via batch jobs

```
rivanna> cd $PROJECT/osmi/benchmark
rivanna> make run
```
*Note: results stored in $PROJECT/osmi/osmi-output directory

<!-- ### Run test sweep via interactive jobs

```
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=01:00:00 --partition=bii-gpu --gres=gpu:v100:1
node> cd $PROJECT/osmi/benchmark
node> singularity run --nv --home `pwd` ../serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &
// wait for lsof -i:8500 to show up
node> python metabench.py $PROJECT/osmi/machine/rivanna/rivanna-V100.yaml
``` -->

### Graphing Results

```
vi $PROJECT/osmi/results.ipynb
```
graphs are also saved in cd $PROJECT/osmi/out

The program takes the results from metabench and produces several graphs.

<!-- ```
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=1-00:00:00 --partition=bii-gpu --gres=gpu
node> singularity shell --nv --home `pwd` serving_latest-gpu.sif
singularity> nvidia-smi #to see if you can use gpus (on node)
singularity> cd benchmark
singularity> tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &
singularity> cat log //to check its working
singularity> lsof -i :8500 // to make sure it an accept incoming directions
```

Edit /project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark/tfs_grpc_client.py to make sure all the models use float32
To run the client:

```
python tfs_grpc_client.py -m [model, e.g. small_lstm] -b [batch size, e.g. 32] -n [# of batches, e.g. 10]  localhost:8500
```

simpler way

```
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=1-00:00:00 --partition=bii-gpu --gres=gpu
conda activate osmi
node> cd /project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark
node> singularity run --nv --home `pwd` ../serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &
node> python tfs_grpc_client.py -m large_tcnn -b 128 -n 100 localhost:8500
```

run with slurm script

```
rivanna> cd /project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark
rivanna> sbatch test_script.slurm
```

Multiple GPU parallelization - incomplete

```
node> singularity exec --bind `pwd`:/home --pwd /home     ../haproxy_latest.sif haproxy -d -f haproxy-grpc.cfg >& haproxy.log &
node> cat haproxy.log
node> CUDA_VISIBLE_DEVICES=0 singularity run --home `pwd` --nv ../serving_latest-gpu.sif tensorflow_model_server --port=8500 --model_config_file=models.conf >& tfs0.log &
node> cat tfs0.log
node> CUDA_VISIBLE_DEVICES=1 singularity run --home `pwd` --nv ../serving_latest-gpu.sif tensorflow_model_server --port=8501 --model_config_file=models.conf >& tfs1.log &
node> cat tf
```

do this for all gpus with different ports -->

## References

1. Production Deployment of Machine-Learned Rotorcraft Surrogate Models on HPC, Wesley Brewer, Daniel Martinez, 
   Mathew Boyer, Dylan Jude, Andy Wissink, Ben Parsons, Junqi Yin, Valentine Anantharaj
   2021 IEEE/ACM Workshop on Machine Learning in High Performance Computing Environments (MLHPC),
   978-1-6654-1124-0/21/$31.00 ©2021 IEEE | DOI: 10.1109/MLHPC54614.2021.00008, <https://ieeexplore.ieee.org/document/9652868>
   TODO: please ask wess what the free pdf link is all gov organizations have one. for example as ornl is coauther it 
   must be on their site somewhere.
   

2. Using Rivanna for GPU ussage, Gregor von Laszewski, JP. Fleischer 
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/hpc/rivanna-introduction.md>

3. Setting up a Windows computer for research, Gregor von Laszewski, J.P Fleischer 
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/windows-configuration.md>
   
4. Initial notes to be deleted, Nate: <https://docs.google.com/document/d/1luDAAatx6ZD_9-gM5HZZLcvglLuk_OqswzAS2n_5rNA>

