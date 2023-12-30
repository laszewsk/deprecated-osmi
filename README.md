# mlcommons-osmi

[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/laszewsk/osmi)
[![GitHub issues](https://img.shields.io/github/issues/laszewsk/osmi.svg)](https://github.com/laszewsk/osmi/issues)
[![Contributors](https://img.shields.io/github/contributors/laszewsk/osmi.svg)](https://github.com/laszewsk/osmi/graphs/contributors)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)](https://www.linux.org/)

## Other Repos

[![General badge](https://img.shields.io/badge/mlcommons-dev-<COLOR>.svg)](https://github.com/laszewsk/mlcommons)
[![General badge](https://img.shields.io/badge/cloudmesh-ee-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh-ee)
[![General badge](https://img.shields.io/badge/cloudmesh-common-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh-common)
[![General badge](https://img.shields.io/badge/cloudmesh-cmd5-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh-cmd5)

## Authors

* Nate Kimball
* Gregor von Laszewski, laszewski@gmail.com, [orcid: 0000-0001-9558-179X](https://orcid.org/0000-0001-9558-179X)

## Table of contents

- [mlcommons-osmi](#mlcommons-osmi)
  - [Other Repos](#other-repos)
  - [Authors](#authors)
  - [Table of contents](#table-of-contents)
  - [1. Running OSMI Bench on macOS natively](#1-running-osmi-bench-on-macos-natively)
    - [1.1 Install and run training](#11-install-and-run-training)
  - [1. Running OSMI Bench on Ubuntu natively](#1-running-osmi-bench-on-ubuntu-natively)
    - [1.1 Create python virtual environment on Ubuntu](#11-create-python-virtual-environment-on-ubuntu)
    - [1.2 Get the code](#12-get-the-code)
    - [1.3 Running the small OSMI model benchmark](#13-running-the-small-osmi-model-benchmark)
    - [1.4 TODO: Install tensorflow serving in ubuntu](#14-todo-install-tensorflow-serving-in-ubuntu)
  - [2. Running on UVA Rivanna](#2-running-on-uva-rivanna)
    - [2.1 Logging into Rivanna](#21-logging-into-rivanna)
    - [2.2 Running OSMI Bench on rivanna](#22-running-osmi-bench-on-rivanna)
    - [2.3 Set up a project directory and get the code](#23-set-up-a-project-directory-and-get-the-code)
    - [2.4 Set up Python Environment](#24-set-up-python-environment)
    - [2.5 Build Tensorflow Serving, Haproxy, and OSMI Images](#25-build-tensorflow-serving-haproxy-and-osmi-images)
    - [2.6 Compile OSMI Models in Batch Jobs](#26-compile-osmi-models-in-batch-jobs)
      - [GREGOR CAME TILL HERE](#gregor-came-till-here)
    - [Run benchmark with cloudmesh experiment executor](#run-benchmark-with-cloudmesh-experiment-executor)
    - [Graphing Results](#graphing-results)
    - [Compile OSMI Models in Interactive Jobs (avpid using)](#compile-osmi-models-in-interactive-jobs-avpid-using)
  - [3. Running on UFL MALTLab](#3-running-on-ufl-maltlab)
    - [3.1 Logging into MALTLab](#31-logging-into-maltlab)
    - [3.2 Running OSMI Bench on maltlab](#32-running-osmi-bench-on-maltlab)
    - [3.3 Set up a project directory and get the code](#33-set-up-a-project-directory-and-get-the-code)
    - [3.4 Running the small OSMI model benchmark](#34-running-the-small-osmi-model-benchmark)
    - [3.5 Build Tensorflow Serving, Haproxy, and OSMI Images](#35-build-tensorflow-serving-haproxy-and-osmi-images)
    - [3.6 Compile OSMI Models in Batch Jobs](#36-compile-osmi-models-in-batch-jobs)
    - [Run benchmark with cloudmesh experiment executor](#run-benchmark-with-cloudmesh-experiment-executor-1)
  - [1. Running OSMI Bench on a local Windows WSL](#1-running-osmi-bench-on-a-local-windows-wsl)
    - [Create python virtual environment on WSL Ubuntu](#create-python-virtual-environment-on-wsl-ubuntu)
    - [Get the code](#get-the-code)
  - [Summit Instructions](#summit-instructions)
  - [References](#references)

## 1. Running OSMI Bench on macOS natively

### 1.1 Install and run training

To install and run training on macOS we conduct three steps

First, we install a version of python that is compatible with tensorflow 
and smartredis

```bash
macOS> 
  python3.10 -m venv ~/OSMI
  source ~/OSMI/bin/activate
  pip install pip -U
```

Second, We check out the code in a OSMI_HOME directory

```
macOS>
  mkdir ./osmi
  export OSMI_HOME=$(realpath "./osmi")
  export OSMI=$OSMI_HOME
  git clone https://github.com/laszewsk/osmi.git
  cd osmi
  pip install -r target/macos/requirements.txt
```

Third, we run the experiments


```bash
macOS>
  cd models
  time python train.py small_lstm  # ~   3.2s on an M1 Max  10 core 64GB and 8.7s on an i5 1135g7
  time python train.py medium_cnn  # ~  13.9s on an M1 Max 10 core 64GB and 20.27s on an i5 1135g7
  time python train.py large_tcnn  # ~ 298.0s on an M1 Max 10 core 64GB 
                                   #   4m 58s
```



## 1. Running OSMI Bench on Ubuntu natively

### 1.1 Create python virtual environment on Ubuntu

Note:
> * tensorflow, 3.10 is the latest supported version
> * smartredis, python 3.10 is the latest supported version
>
> * Hence, we will use python3.10

First create a venv with 

```bash
ubuntu> 
  python3.10 -m venv ~/OSMI
  source ~/OSMI/bin/activate
  pip install pip -U
```

### 1.2 Get the code

We assume that you go to the directory where you want to install `osmi`. We assume you do not have a directory called osmi in it. Use simply `ls osmi` to check. Next we set up the osmi directory and clone it from github.
To get the code we clone this github repository

<https://github.com/laszewsk/osmi.git>

Please execute:

```
ubuntu>
  mkdir ./osmi
  export OSMI_HOME=$(realpath "./osmi")
  export OSMI=$(OSMI_HOME)/
  git clone https://github.com/laszewsk/osmi.git
  cd osmi
  pip install -r target/ubuntu/requirements-ubuntu.txt
```

### 1.3 Running the small OSMI model benchmark

```bash
ubuntu>
  cd models
  time python train.py small_lstm  # ~   4.9s on an 5950X with RTX3090
  time python train.py medium_cnn  # ~  34.0s on an 5950X with RTX3090
  time python train.py large_tcnn  # ~ 16m58s on an 5950X with RTX3090
```

### 1.4 TODO: Install tensorflow serving in ubuntu

This documentation is unclear and not tested:

> Unclear. the documentation do this with singularity, I do have
> singularity on desktop, but can we use it natively and compare with
> singularity performance?

> ```
> echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list
> curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -
> sudo apt-get update && sudo apt-get install tensorflow-model-server
> which tensorflow_model_server
>make image
> ```


## 2. Running on UVA Rivanna

### 2.1 Logging into Rivanna

The easiest way to log into rivanna is to use ssh. However as we are
creating singularity images, we need to currently use either bihead1 or bihead2

Please follow the documentation at

<http://sciencefmhub.org/docs/tutorials/rivanna/singularity/>

to set this up

Best is to also install cloudmesh-rivanna and cloudmesh-vpn on your
local machine, so that login and management of the machine is
simplified

```bash
local>
  python -m venv ~/ENV3
  pip install cloudmesh-rivanna
  pip install cloudmesh-vpn
```

In case you have set up the vpn client correctly you can now activate
it from the terminal including gitbash on windows. If this does not
work, you can alternatively just use the cisco vpn gu client and ssh
to one of biheads.

In case you followed our documentation you will be able to say


```bash
local>
  cms vpn activate
  ssh b1
```

Furthermore we assume that you have the code also checked out on your
laptop as we use this to sync later on the results created with the
super computer.


```bash
local>
  mkdir ~/github
  cd ~/github
  git clone git clone https://github.com/laszewsk/osmi.git
  cd osmi
```

To have the same environment variables to access the code on rivanna
we introduce

```bash
local>
  export USER_SCRATCH=/scratch/$USER
  export USER_LOCALSCRATCH=/localscratch/$USER
  export BASE=$USER_SCRATCH
  export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
  export PROJECT=$BASE/osmi
  export EXEC_DIR=$PROJECT/target/rivanna
```

This will come in handy when we rsync the results.
Now you are logged in on  frontend node to rivanna.



### 2.2 Running OSMI Bench on rivanna

To run the OSMI benchmark, you will first need to generate the project
directory with the code. We assume you are in the group
`bii_dsc_community`, and

SOME OTHERS MISSING COPY FROM OUR DOCUMENTATION

so you can create singularity images on rivanna.


<!-- This allows you access to the directory
```/project/bii_dsc_community```-->

As well as the slurm partitions `gpu` and `bii_gpu`

We will set up OSMI in the /scratch/$USER directory.

### 2.3 Set up a project directory and get the code

<!-- To get the code we clone a gitlab instance that is hosted at -->
<!-- Oakridge National Laboratory -->
<!-- (<https://code.ornl.gov/whb/osmi-bench>). -->


First you need to create the directory. The following steps simplify
it and make the instalation uniform.


<!--
b1>
  export USER_PROJECT=/project/bii_dsc_community/$USER
  export BASE=$USER_PROJECT
-->

```
b1>
  export USER_SCRATCH=/scratch/$USER
  export USER_LOCALSCRATCH=/localscratch/$USER
  export BASE=$USER_SCRATCH
  export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
  export PROJECT=$BASE/osmi
  export EXEC_DIR=$PROJECT/target/rivanna

  mkdir -p $BASE
  cd $BASE
  git clone https://github.com/laszewsk/osmi.git
  cd osmi
```

You now have the code in `$PROJECT`


### 2.4 Set up Python Environment

Note: This is no longer working

> OSMI will run in batch mode this is also valid for setting up the
> environment for which we created sbatch script.  This has the
> advantage that it installed via the worker nodes, which is typically
> faster, but also gurantees that the worker node itself is ued to
> install it to avoid software incompatibilities.
>
> ```
> b1>
>  cd $EXEC_DIR
>  sbatch environment.slurm
>  # (this may take a while)
>  source $BASE/ENV3/bin/activate
> ```
>
> See: [environment.slurm](https://github.com/laszewsk/osmi/blob/main/target/rivanna/environment.slurm)

Note: currently we recommend this way:

An alternate way is to run the following commands directly:

```
b1>
  cd $EXEC_DIR
  module load gcc/11.4.0  openmpi/4.1.4 python/3.11.4
  which python
  python --version
  python -m venv $BASE/ENV3 # takes about 5.2s
  source $BASE/ENV3/bin/activate
  pip install pip -U
  time pip install -r $EXEC_DIR/requirements.txt # takes about 1m21s
  cms help
```



### 2.5 Build Tensorflow Serving, Haproxy, and OSMI Images

We created convenient singularity images for tensorflow serving,
haproxy, and the code to be executed. This is done with


```
b1>
  cd $EXEC_DIR
  make images
```


### 2.6 Compile OSMI Models in Batch Jobs

To run some of the test jobs to run a model and see if things work you
can use the commands

```
b1>
  cd $EXEC_DIR
  sbatch train-small.slurm  #    26.8s on a100_80GB, bi_fox_dgx
  sbatch train-medium.slurm #    33.5s on a100_80GB, bi_fox_dgx
  sbatch train-large.slurm  # 1m  8.3s on a100_80GB, bi_fox_dgx
```


#### GREGOR CAME TILL HERE 

### Run benchmark with cloudmesh experiment executor

Set parameters in config.in.slurm

```
experiment:
  # different gpus require different directives
  directive: "a100,v100"
  # batch size
  batch: "1,2,4,8,16,32,64,128"
  # number of gpus
  ngpus: "1,2,3,4"
  # number of concurrent clients
  concurrency: "1,2,4,8,16"
  # models
  model: "small_lstm,medium_cnn,large_tcnn"
  # number of repetitions of each experiment
  repeat: "1,2,3,4"
```

To run many different jobs that are created based on config.in.slurm
You can use the following

```
b1>
  cd $EXEC_DIR
  make project-gpu
  sh jobs-project-gpu.sh
```

The results will be stored in a projects directory.

### Graphing Results

To analyse the program it is best to copy the results into your local
computer and use a jupyter notebook.

```
local>
  cd ~/github/osmi/target/rivanna
  du -h rivanna:$EXEC_DIR/project-gpu
  // figure out if you have enough space for this project on the local machine
  rsync rivanna:$EXEC_DIR/project-gpu ./project-gpu
```

Now we can analyse the data with 

```
local>
  open ./analysis/analysis-simple.ipynb
```

graphs are also saved in `./analysis/out`

The program takes the results from clodmesh experiment executir and
produces several graphs.





### Compile OSMI Models in Interactive Jobs (avpid using)

**Interactive Jobs:** allow you to reserve a node on rivanna so it
looks like a login node. This interactive mode is usefull only during
the debug phase and can serve as a convenient way to debug and to
interactively experiment running the program.

Once you know hwo to create jobs with a propper batch script you will
likely no longer need to use interactive jobs. We keep this
documentation for beginners that like to experiement in interactive
mode to develop batch scripts.

First, obtain an interactive job with

```
rivanna>
  ijob -c 1 -A bii_dsc_community -p standard --time=01:00:00
```

To specify a particular GPU please use. 

```
rivanna>
  export GPUS=1
  v100 rivanna> ijob -c 1 -A bii_dsc_community --partition=bii-gpu --gres=gpu:v100:$GPUS --time=01:00:00
  # (or)
  a100 rivanna> ijob -c 1 -A bii_dsc_community --partition=bii-gpu --gres=gpu:a100:$GPUS --time=01:00:00
```


```
node>
  cd $PROJECT/models
  python train.py small_lstm
  python train.py medium_tcnn
  python train.py large_cnn
```

For this application there is no separate data


## 3. Running on UFL MALTLab

### 3.1 Logging into MALTLab

The easiest way to log into maltlab is to use ssh.

Best is to also install cloudmesh-vpn on your
local machine, so that login and management of the machine is
simplified

```bash
local>
  python -m venv ~/ENV3

  # windows
  source ~/ENV3/Scripts/activate
  # other os
  source ~/ENV3/bin/activate

  pip install cloudmesh-vpn
```

In case you have set up the vpn client correctly you can now activate
it from the terminal including gitbash on windows. If this does not
work, you can alternatively just use the cisco vpn gu client and ssh
to one of biheads.

In case you followed our documentation you will be able to say


```bash
local>
  cms vpn connect --service=ufl
  # you need to set up maltlab.cise.ufl.edu in your ~/.ssh/config.
  ssh maltlab
```

Furthermore we assume that you have the code also checked out on your
laptop as we use this to sync later on the results created with the
super computer.


```bash
local>
  mkdir ~/github
  cd ~/github
  git clone https://github.com/laszewsk/osmi.git
  cd osmi
```

To have the same environment variables to access the code on maltlab
we introduce

```bash
local>
  # you probably have a different username :)
  export USER=jpf

  export USER_SCRATCH=/mnt/hdd/$USER/scratch
  # export USER_LOCALSCRATCH=/localscratch/$USER
  export BASE=$USER_SCRATCH
  export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
  export PROJECT=$BASE/osmi
  export EXEC_DIR=$PROJECT/target/maltlab
```

This will come in handy when we rsync the results.
Now you are logged in on maltlab.


### 3.2 Running OSMI Bench on maltlab

To run the OSMI benchmark, you will first need to generate the project
directory with the code.


<!-- This allows you access to the directory
```/project/bii_dsc_community```-->


We will set up OSMI in the /home/$USER/scratch directory.

### 3.3 Set up a project directory and get the code

<!-- To get the code we clone a gitlab instance that is hosted at -->
<!-- Oakridge National Laboratory -->
<!-- (<https://code.ornl.gov/whb/osmi-bench>). -->


First you need to create the directory. The following steps simplify
it and make the instalation uniform.


<!--
b1>
  export USER_PROJECT=/project/bii_dsc_community/$USER
  export BASE=$USER_PROJECT
-->

```bash
maltlab>
  # you probably have a different username :)
  export USER=jpf

  export USER_SCRATCH=/mnt/hdd/$USER/scratch
  # export USER_LOCALSCRATCH=/localscratch/$USER
  export BASE=$USER_SCRATCH
  export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
  export PROJECT=$BASE/osmi
  export EXEC_DIR=$PROJECT/target/maltlab

  mkdir -p $BASE
  cd $BASE
  git clone https://github.com/laszewsk/osmi.git
  cd osmi
  git checkout training
```

You now have the code in `$PROJECT`

### 3.4 Running the small OSMI model benchmark

```bash
maltlab>
  cd models
  time python train.py small_lstm  # ~   4.9s on an 5950X with RTX3090
  time python train.py medium_cnn  # ~  34.0s on an 5950X with RTX3090
  time python train.py large_tcnn  # ~ 16m58s on an 5950X with RTX3090
```

Now we consider using slurm and batch ee execution


```bash
maltlab>
  cd $EXEC_DIR
  
  python3.11 -m venv $BASE/ENV3 # takes about 5.2s
  source $BASE/ENV3/bin/activate
  pip install pip -U
  time pip install -r $EXEC_DIR/requirements.txt # takes about 1m21s
  cms help
```

### 3.5 Build Tensorflow Serving, Haproxy, and OSMI Images

We created convenient singularity images for tensorflow serving,
haproxy, and the code to be executed. This is done with


```
maltlab>
  cd $EXEC_DIR
  make images
```


### 3.6 Compile OSMI Models in Batch Jobs

To run some of the test jobs to run a model and see if things work you
can use the commands

```
maltlab>
  cd $EXEC_DIR
  sbatch train-small.slurm  #    26.8s on a100_80GB, bi_fox_dgx
  sbatch train-medium.slurm #    33.5s on a100_80GB, bi_fox_dgx
  sbatch train-large.slurm  # 1m  8.3s on a100_80GB, bi_fox_dgx
```

### Run benchmark with cloudmesh experiment executor

Set parameters in config.in.yaml

```
experiment:
  # different gpus require different directives
  directive: "a100,v100"
  # batch size
  batch: "1,2,4,8,16,32,64,128"
  # number of gpus
  ngpus: "1,2,3,4"
  # number of concurrent clients
  concurrency: "1,2,4,8,16"
  # models
  model: "small_lstm,medium_cnn,large_tcnn"
  # number of repetitions of each experiment
  repeat: "1,2,3,4"
```

To run many different jobs that are created based on config.in.slurm
You can use the following

```
maltlab>
  cd $EXEC_DIR
  make project
  sh project-jobs.sh
```

The results will be stored in a projects directory.

<!-- end jp -->


## 1. Running OSMI Bench on a local Windows WSL

TODO: Nate

1. create isolated new wsl environment
2. Use what we do in the ubuntu thing, but do separate documentation
   er as the ubuntu native install may have other steps or issuse


### Create python virtual environment on WSL Ubuntu

```
wsl> python3.10 -m venv /home/$USER/OSMI
  source /home/$USER/OSMI/bin/activate
  python -V
  pip install pip -U
```

### Get the code

To get the [code](<https://code.ornl.gov/whb/osmi-bench>) we clone a
gitlab instance that is hosted at Oakridge National Laboratory,
please execute:

```
wsl>
  export PROJECT=/home/$USER/project/
  mkdir -p $PROJECT
  cd $PROJECT
  git clone https://github.com/laszewsk/osmi #git@github.com:laszewsk/osmi.git
  cd osmi/
  pip install -r $PROJECT/mlcommons-osmi/wsl/requirements.txt
```


```
wsl>
  cd $PROJECT/mlcommons-osmi/wsl
  make image
  cd models
  time python train.py small_lstm (14.01s user 1.71s system 135% cpu 11.605 total)
  time python train.py medium_cnn (109.20s user 6.84s system 407% cpu 28.481 total)
  time python train.py large_tcnn
  cd .. 
```

<!--


----------------------------------------------------------------------

```
rivanna> 
  ijob -c 1 -A bii_dsc_community -p standard --time=1-00:00:00 --partition=bii-gpu --gres=gpu
node> 
  singularity shell --nv --home `pwd` serving_latest-gpu.sif
  singularity> nvidia-smi #to see if you can use gpus (on node)
  singularity> cd benchmark
  singularity> tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &
  singularity> cat log //to check its working
  singularity> lsof -i :8500 // to make sure it an accept incoming directions
```

Edit
/project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark/tfs_grpc_client.py
to make sure all the models use float32 To run the client:

```
python tfs_grpc_client.py -m [model, e.g. small_lstm] -b [batch size, e.g. 32] -n [# of batches, e.g. 10]  localhost:8500
```

simpler way

```
rivanna> 
  ijob -c 1 -A bii_dsc_community -p standard --time=1-00:00:00 --partition=bii-gpu --gres=gpu
  conda activate osmi
node> 
  cd /project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark
  singularity run --nv --home `pwd` ../serving_latest-gpu.sif tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& log &
  python tfs_grpc_client.py -m large_tcnn -b 128 -n 100 localhost:8500
```

run with slurm script

```
rivanna> 
  cd /project/bii_dsc_community/$USER/osmi/osmi-bench/benchmark
  sbatch test_script.slurm
```

Multiple GPU parallelization - incomplete

```
node> 
  singularity exec --bind `pwd`:/home --pwd /home     ../haproxy_latest.sif haproxy -d -f haproxy-grpc.cfg >& haproxy.log &
  cat haproxy.log
  CUDA_VISIBLE_DEVICES=0 singularity run --home `pwd` --nv ../serving_latest-gpu.sif tensorflow_model_server --port=8500 --model_config_file=models.conf >& tfs0.log &
  cat tfs0.log
  CUDA_VISIBLE_DEVICES=1 singularity run --home `pwd` --nv ../serving_latest-gpu.sif tensorflow_model_server --port=8501 --model_config_file=models.conf >& tfs1.log &
  cat tf
```

do this for all gpus with different ports

----------------------------------------------------------------------

-->

## Summit Instructions


1. Install software

```bash
summit>
  git clone https://code.ornl.gov/whb/osmi-bench.git
```

2. Get interactive debug node

```bash
summit>
  export PROJ_ID=ABC123 # change ABC123 to your project number
  bsub -Is -q debug -P ${PROJ_ID} -nnodes 1 -W 1:00 -J osmi $SHELL
```
3. Setup environment

```bash
summit>
  cd osmi-bench
  . benchmark/env.sh
```

4. Train models

```bash
summit>
  cd models
  jsrun -n1 python train.py small_lstm
  jsrun -n1 python train.py medium_cnn
  jsrun -n1 python train.py large_tcnn
```

Note: Edit benchmark/models.conf to modify paths to point to the individual, e.g., /ccs/home/whbrewer/osmi-bench/models/small_lstm

5. Start up tensorflow model server

```bash
summit>
  jsrun -n1 tensorflow_model_server --port=8500 --rest_api_port=0 --model_config_file=models.conf >& $MEMBERWORK/$PROJ_ID/tfs.log &
```

6. Test that server is running

```bash
summit>
  jsrun -n1 lsof -i :8500
```

7. Test benchmark

```bash
summit>
  jsrun -n1 python tfs_grpc_client.py -m small_lstm -b 32 -n 10 localhost:8500
```

## References

1. Production Deployment of Machine-Learned Rotorcraft Surrogate
   Models on HPC, Wesley Brewer, Daniel Martinez, Mathew Boyer, Dylan
   Jude, Andy Wissink, Ben Parsons, Junqi Yin, Valentine Anantharaj
   2021 IEEE/ACM Workshop on Machine Learning in High Performance
   Computing Environments (MLHPC), 978-1-6654-1124-0/21/$31.00 ©2021
   IEEE | DOI: 10.1109/MLHPC54614.2021.00008,
   <https://ieeexplore.ieee.org/document/9652868> TODO: please ask
   wess what the free pdf link is all gov organizations have one. for
   example as ornl is coauther it must be on their site somewhere.

2. Wes Brewer, OSMI-bench, <https://code.ornl.gov/whb/osmi-bench>

3. Using Rivanna for GPU ussage, Gregor von Laszewski, JP. Fleischer
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/hpc/rivanna-introduction.md>

4. Setting up a Windows computer for research, Gregor von Laszewski,
   J.P Fleischer
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/windows-configuration.md>
   
5. Initial notes to be deleted, Nate:
   <https://docs.google.com/document/d/1luDAAatx6ZD_9-gM5HZZLcvglLuk_OqswzAS2n_5rNA>

6. Gregor von Laszewski, J.P. Fleischer, Cloudmesh VPN, 
   <https://github.com/cloudmesh/cloudmesh-vpn>

7. Gregor von Laszewski, Cloudmesh Rivanna, 
   <https://github.com/cloudmesh/cloudmesh-rivanna>

8. Gregor von Laszewski, Cloudmesh Common, 
   <https://github.com/cloudmesh/cloudmesh-common>

9. Gregor von Laszewski, Cloudmesh Experiment Executor, 
   <https://github.com/cloudmesh/cloudmesh-ee>

10.  Gregor von Laszewski, J.P. Fleischer, Geoffrey C. Fox, Juri Papay,
    Sam Jackson, Jeyan Thiyagalingam (2023).  Templated Hybrid
    Reusable Computational Analytics Workflow Management with
    Cloudmesh, Applied to the Deep Learning MLCommons Cloudmask
    Application. eScience'23.
    <https://github.com/cyberaide/paper-cloudmesh-cc-ieee-5-pages/raw/main/vonLaszewski-cloudmesh-cc.pdf>, 2023.

11. Gregor von Laszewski, J.P. Fleischer, R. Knuuti, G.C. Fox,
    J. Kolessar, T.S. Butler, J. Fox (2023). Opportunities for
    enhancing MLCommons efforts while leveraging insights from
    educational MLCommons earthquake benchmarks efforts. Frontiers in
    High Performance Computing.
	  <https://doi.org/10.3389/fhpcp.2023.1233877>
