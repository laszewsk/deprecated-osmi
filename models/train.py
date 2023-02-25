"""usage: python train.py {small_lstm|medium_cnn|large_tcnn}"""
import argparse
import importlib
import numpy as np
import os
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from cloudmesh.common.StopWatch import StopWatch

parser = argparse.ArgumentParser()
archs = [s.split('.')[0] for s in os.listdir('archs') if s[0:1] != '_']
parser.add_argument('arch', type=str, choices=archs, help='Type of neural network architectures')
args = parser.parse_args()

def start(msg):
    StopWatch.start(f"train-py {msg} arch={args.arch}, input_shape={input_shape}, output_shape={output_shape}")
    
def stop(msg):
    StopWatch.stop(f"train-py {msg} arch={args.arch}, input_shape={input_shape}, output_shape={output_shape}")
    
# parameters
samples = 100 
epochs = 5
batch_size = 32

# compute synthetic data for X and Y
if args.arch == "small_lstm":
    input_shape = (8, 48)
    output_shape = (2, 12)
elif args.arch == "medium_cnn":
    input_shape = (101, 82, 9)
    output_shape = (101, 82)
elif args.arch == "large_tcnn":
    input_shape = (3, 101, 82, 9)
    output_shape = (3, 101, 82, 1)
else:
    raise ValueError("Model not supported. Need to specify input and output shapes")

start("create data")
X = np.random.rand(samples, *input_shape)
Y = np.random.rand(samples, *output_shape)
stop("create data")

# define model
start("define model")
model = importlib.import_module('archs.' + args.arch).build_model(input_shape)
model.summary()
stop("define model")

# compile model
start("compile model")
model.compile(loss='mae', optimizer='adam')
stop("compile model")

# train model
start("train model")
model.fit(X, Y, batch_size=batch_size, epochs=epochs)
stop("train model")

start("save model")
model.save(f"{args.arch}/1")
stop("save model")

StopWatch.benchmark()
