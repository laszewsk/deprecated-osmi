import argparse
import numpy as np
import time
from tqdm import tqdm
from cloudmesh.common.StopWatch import StopWatch

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--batch', type=int, default=1, help='batch size')
parser.add_argument('-m', '--model', required=True, default='medium_cnn', type=str)
parser.add_argument('-n', '--num_requests', default=128, type=int, help='number of requests')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
args = parser.parse_args()

def start(msg):
    StopWatch.start(f"benchmark-py {msg} model={args.model}, batch={args.batch}, num_requests={args.num_requests}")

def stop(msg):
    StopWatch.stop(f"benchmark-py {msg} model={args.model}, batch={args.batch}, num_requests={args.num_requests}")
# Local imports
from models import models
from smi import SMI


# gRPC
start("retrieve model")
inference = SMI(model=args.model, hostport='localhost:8500').grpc(args.batch)
stop("retrieve model")

# HTTP
#inference = SMI(model=args.model, hostport='localhost:8501').http()

# Embedded
#inference = SMI(model=args.model).embedded(model_base_path="/ccs/home/whbrewer/surbench/models")

start("define model params")
meta = models(args.batch)[args.model]
input_shape = meta['input_shape']
output_name = meta['output_name']
output_shape = meta['output_shape']
dtype_name = meta['dtype'].__name__
dtype_map = {'float64': 'double_val', 'float32': 'float_val'}
dtype_method = dtype_map[dtype_name]
stop("define model params")

times = []
for _ in tqdm(range(args.num_requests)):
    start("create data")
    data = np.array(np.random.random(input_shape))
    stop("create data")
    tik = time.perf_counter()
    start("inference")
    result = inference(data)
    stop("inference")
    tok = time.perf_counter()
    if args.verbose:
        # following is for gRPC output
        print(np.reshape(getattr(result.outputs[output_name], dtype_method), output_shape))
    times.append(tok-tik)
   
elapsed = sum(times)
average = elapsed/args.num_requests
print(f"elapsed: {elapsed:.4f}s, avg: {average:.4f}s")
StopWatch.event("benchmark result", {"elapsed": elapsed, "average": average})
StopWatch.benchmark()
