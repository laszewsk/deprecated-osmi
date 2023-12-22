"""
Usage:
     train.py [--samples=SAMPLES] [--epochs=EPOCHS] [--batch_size=BATCH_SIZE] ARCH
    
This executs the training for OSMI.
    
Arguments:
    ARCH   the model architecture. Allowed values small_lstm, medium_cnn, large_tcnn
    
Options:
    --samples=SAMPLES           number of samples to generate
    --epochs=EPOCHS             number of epochs to train
    --batch_size=BATCH_SIZE     the batch size
    
Description:
    TBD
"""
import argparse
import importlib
import numpy as np
import os
import tensorflow as tf
import docopt

from tensorflow import keras
from tensorflow.keras import layers
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import banner
from cloudmesh.common.debug import VERBOSE


StopWatch.start("total")

args = docopt.docopt(__doc__)

# define hyperparameters
arch = args["ARCH"] or "small_lstm"
samples = int(args["--samples"] or 100)
epochs = int(args["--epochs"] or 5)
batch_size = int(args["--batch_size"] or 32)

# compute synthetic data for X and Y
if arch == "small_lstm":
    input_shape = (8, 48)
    output_shape = (2, 12)
elif arch == "medium_cnn":
    input_shape = (101, 82, 9)
    output_shape = (101, 82)
elif arch == "large_tcnn":
    input_shape = (3, 101, 82, 9)
    output_shape = (3, 101, 82, 1)
else:
    raise ValueError("Model not supported. Need to specify input and output shapes")


event = {
    "input_shape": input_shape,
    "output_shape": output_shape
}
StopWatch.event("configuration", event)

StopWatch.start("core")

StopWatch.start("create data")
X = np.random.rand(samples, *input_shape)
Y = np.random.rand(samples, *output_shape)
StopWatch.stop("create data")

# define model
StopWatch.start("define model")
model = importlib.import_module('archs.' + arch).build_model(input_shape)
model.summary()
StopWatch.stop("define model")

# compile model
StopWatch.start("compile model")
model.compile(loss='mae', optimizer='adam')
StopWatch.stop("compile model")

# train model
StopWatch.start("train model")
model.fit(X, Y, batch_size=batch_size, epochs=epochs)
StopWatch.stop("train model")


StopWatch.start("save model")
model.save(f"{arch}/1")
StopWatch.stop("save model")

StopWatch.stop("core")

StopWatch.stop("total")

StopWatch.benchmark(tag=arch)
