#!/usr/bin/env bash


PROJECT_DIR=../../../../..


#MODELS_DIR=$PROJECT_DIR/models
MODELS_DIR=./models


RESULT_DIR=`pwd`


# PYTHON_DIR=~OSMI
# source $PYTHON_DIR/bin/activate
echo "============================================================"
echo "PROJECT_ID: {identifier}"
echo "MODELS_DIR: $MODELS_DIR"
echo "MODEL: {experiment.model}"
echo "REPEAT: {experiment.repeat}"

cd $MODELS_DIR
time python train.py {experiment.model} > $RESULT_DIR/osmi-{identifier}-$USER-$PID.out

# > $RESULT_DIR/log.txt 2>&1

