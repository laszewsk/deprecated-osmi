#!/usr/bin/env bash

PROJECT_DIR=../../../../..
MODELS_DIR=./models
RESULT_DIR=`pwd`
OUTPUT=$RESULT_DIR/osmi-{identifier}-$USER-$PID.out


# PYTHON_DIR=~/OSMI
# source $PYTHON_DIR/bin/activate
echo "============================================================"
echo "PROJECT_ID: {identifier}"
echo "MODELS_DIR: $MODELS_DIR"
echo "MODEL: {experiment.model}"
echo "REPEAT: {experiment.repeat}"

FLAGS="--ipc=host --ulimit memlock=-1 --ulimit stack=67108864"
BIND="--mount type=bind,source=$(pwd),target=$(pwd)"

cd $MODELS_DIR

docker run --workdir=$(pwd) -it --gpus=all $FLAGS $BIND  osmi_train  python train.py {experiment.model} > $OUTPUT

#	docker run -it --gpus=all --mount $BIND osmi_train bash
tr -cd '\11\12\15\40-\176' < $OUTPUT > tmp-output
mv tmp-output $OUTPUT
