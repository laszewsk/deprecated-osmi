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
2. use what we do in the ubuntu thing, but do separate documentation
   er as the ubuntu native install may have other steps or issuse


### Create python virtual environment on WSL Ubuntu

```
wsl> python3 -m venv /home/$USER/OSMI
wsl> source /home/$USER/OSMI/bin/activate
wsl> python -V
wsl> pip install pip -U
```

### Get the code

To get the [code](<https://code.ornl.gov/whb/osmi-bench>) we clone a
gitlab instance that is hosted at Oakridge National Laboratory,
please execute:

```
export PROJECT=/home/$USER/project/
mkdir -p $PROJECT
cd $PROJECT
git clone https://github.com/laszewsk/osmi #git@github.com:laszewsk/osmi.git
cd osmi/
pip install -r $PROJECT/mlcommons-osmi/wsl/requirements.txt
```


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

To get the code we clone this github repository
(https://github.com/laszewsk/osmi.git). Please execute:

```
mkdir ~/osmi
cd ~/osmi
git clone https://github.com/laszewsk/osmi.git
cd osmi
pip install -r ~/osmi/osmi/machine/ubuntu/requirements-ubuntu.txt
```

**Note:** the original version of grpcio 1.0.0 does not distribute
valid wheels, hence we assume the library is out of date, but a new
version with 1.15.1 is available that is distributed. Gregor
strongly recoomnds to swithc to a supported version of grpcio.

### Running the small OSMI model benchmark

```
cd models
time python train.py small_lstm  # taks about 10s on an 5950X
time python train.py medium_cnn  # taks less the 12s on an 5950X
time python train.py large_tcnn  # takes less the 30s on an 5950X
```

### Install tensorflow serving in ubuntu

Unclear. the documentation do this with singularity, I do have
singularity on desktop, but can we use it natively and compare with
singularity performance?

Nate will explore theoretically how to isntall tensorflow servving on
ubuntu

compare if others have install instructions, these are old from 16.01
but we want 21. ...

```
sudo pip install tensorflow-serving-api
echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install tensorflow-model-server
which tensorflow_model_server
make image
```

<!--
### Running the program (obsolete)

```
cd ~/osmi/osmi/machine/ubuntu
make run
python metabench.py --config=make-yaml-file-for-ubuntu
```
TODO: complete
-->

## Running on rivanna

### Logging into rivanna

The easiest way to log into rivanna is to use ssh. However as we are
creating singularity images, we need to use either bihead1 or bihead2

Please follow the documentation at

LINK MISSING

to set this up

Best is to also install cloudmesh-rivanna and cloudmesh-vpn on your
local machine, so that login and management of the machine is
simplified

```
local> python -m venv ~/ENV3
local> pip install cloudmesh-rivanna
local> pip install cloudmesh-vpn
```

IN case you have set up the vpn client correctly you can now activate
it from the terminal including gitbash on windows. If this does not
work, you can alternatively just use the cisco vpn gu client and ssh
to one of biheads.

In case you followed our documentation you will be able to say


```
local> cms vpn activate
local> ssh b1
```

Furthermore we assume that you have the code also checked out on your
laptop as we use this to sync later on the results created with the
super computer.


```
local>
  mkdir ~/github
  cd ~/github
  git clone git clone https://github.com/laszewsk/osmi.git
  cd osmi
```

To have the same environment variables to access the code on rivanna
we introduce

```
local>
  export USER_SCRATCH=/scratch/$USER
  export USER_LOCALSCRATCH=/localscratch/$USER
  export BASE=$USER_SCRATCH
  export CLOUDMESH_CONFIG_DIR=$BASE/.cloudmesh
  export PROJECT=$BASE/osmi
  export EXEC_DIR=$PROJECT/target/rivanna
```

This will come in handy when we rsync the results


Now you are looged in on  frontend node to rivanna.



### Running OSMI Bench on rivanna

To run the OSMI benchmark, you will first need to generate the project
directory with the code. We assume you are in the group
`bii_dsc_community`, and

SOME OTHERS MISSING COPY FROM OUR DOCUMENTATION

so you can create singularity images on rivanna.


<!-- This allows you access to the directory
```/project/bii_dsc_community```-->

As well as the slurm partitions `gpu` and `bii_gpu`

We will set up OSMI in the /scratch/$USER directory.

### Set up a project directory and get the code

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


### Set up Python Environment

OSMI will run in batch mode this is also valid for setting up the
environment for which we created abatch script.  This has the
advantage that it installed via the worker nodes, which is typically
faster, but also gurantees that the worker node itself is ued to
install it to avoid software incompatibilities.

```
b1> cd $EXEC_DIR
b1> sbatch environment.slurm
(this may take a while)
b1> source $BASE/ENV3/bin/activate
```

An alternate way is to experiment with the setup on the login node in
acse you like to explore other libraries. However  once you find other
improvements, you ought to include them in the batch script. Here is
what the batch script does internaly.

[environment.slurm](https://github.com/laszewsk/osmi/blob/main/target/rivanna/environment.slurm)

It basically executes the following.

```
b1> cd $EXEC_DIR
b1> module load gcc/11.2.0 openmpi/4.1.4 python/3.11.1
b1> python -m venv $BASE/ENV3
(this may take a while to finish due to rivanna's slow file system)
b1> source $BASE/ENV3/bin/activate
pip install pip -U
pip install -r $EXEC_DIR/requirements.txt
cms help
```



### Build Tensorflow Serving, Haproxy, and OSMI Images

We created convenient singularity images for tensorflow serving,
haproxy, and the code to be executed. This is done with


```
b1> cd $EXEC_DIR
b1> make images
```


### Compile OSMI Models in Batch Jobs

To run some of the test jobs to run a model and see if things work you
can use the commands

```
b1> cd $EXEC_DIR
b1> sbatch train-small.slurm
b1> sbatch train-medium.slurm
b1> sbatch train-large.slurm
```

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
b1> cd $EXEC_DIR
b1> make project-gpu
b1> sh jobs-project-gpu.sh
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
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=01:00:00
```

To specify a particular GPU please use. 

```
export GPUS=1
v100 rivanna> ijob -c 1 -A bii_dsc_community --partition=bii-gpu --gres=gpu:v100:$GPUS --time=01:00:00
a100 rivanna> ijob -c 1 -A bii_dsc_community --partition=bii-gpu --gres=gpu:a100:$GPUS --time=01:00:00
```


```
node> cd $PROJECT/models
node> python train.py small_lstm
node> python train.py medium_tcnn
node> python train.py large_cnn
```

For this application there is no separate data



<!--


----------------------------------------------------------------------

```
rivanna> ijob -c 1 -A bii_dsc_community -p standard --time=1-00:00:00 --partition=bii-gpu --gres=gpu
node> singularity shell --nv --home `pwd` serving_latest-gpu.sif
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

do this for all gpus with different ports

----------------------------------------------------------------------

-->

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
   

2. Using Rivanna for GPU ussage, Gregor von Laszewski, JP. Fleischer
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/hpc/rivanna-introduction.md>

3. Setting up a Windows computer for research, Gregor von Laszewski,
   J.P Fleischer
   <https://github.com/cybertraining-dsc/reu2022/blob/main/project/windows-configuration.md>
   
4. Initial notes to be deleted, Nate:
   <https://docs.google.com/document/d/1luDAAatx6ZD_9-gM5HZZLcvglLuk_OqswzAS2n_5rNA>

5. Gregor von Laszewski, J.P. Fleischer, Cloudmesh VPN, <https://github.com/cloudmesh/cloudmesh-vpn>

6. Gregor von Laszewski, Cloudmesh Rivanna, <https://github.com/cloudmesh/cloudmesh-rivanna>

7. Gregor von Laszewski, Cloudmesh Common, <https://github.com/cloudmesh/cloudmesh-common>

8. Gregor von Laszewski, Cloudmesh Experiment Executor, <https://github.com/cloudmesh/cloudmesh-ee>

9.  Gregor von Laszewski, J.P. Fleischer, Geoffrey C. Fox, Juri Papay,
    Sam Jackson, Jeyan Thiyagalingam (2023).  Templated Hybrid
    Reusable Computational Analytics Workflow Management with
    Cloudmesh, Applied to the Deep Learning MLCommons Cloudmask
    Application. eScience'23.
    <https://github.com/cyberaide/paper-cloudmesh-cc-ieee-5-pages/raw/main/vonLaszewski-cloudmesh-cc.pdf>, 2023.

10. Gregor von Laszewski, J.P. Fleischer, R. Knuuti, G.C. Fox,
    J. Kolessar, T.S. Butler, J. Fox (2023). Opportunities for
    enhancing MLCommons efforts while leveraging insights from
    educational MLCommons earthquake benchmarks efforts. Frontiers in
    High Performance Computing.
	<https://doi.org/10.3389/fhpcp.2023.1233877>
