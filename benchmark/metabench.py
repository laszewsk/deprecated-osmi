"""
Example usage:

Start servers on multiple GPUs:

    ./1_start_tfs_servers.sh

Then run this code e.g. to use 2 GPUs with a sweep of concurrencies 1 2 4 8 16 per GPU:

    export CUDA_VISABLE_DEVICES=0,1
    python metabench.py localhost -g T4 -b 64 -c 1 2 4 8 16 --ports 8500 8501 8502 8503 -n 2

or, can use a YAML file to specify all the options, e.g.:

    python metabench.py rivanna-v100.yaml -o results-v100.csv

"""

import argparse
import csv
import datetime
import glob
import os
import re
import subprocess
import time
import yaml
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.Shell import Shell

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Where to store intermediate files
out_path = "."
#out_path = os.environ['WORKDIR']

# Grab the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('server', help='server ip:port, e.g. 10.1.1.37:8080')
parser.add_argument('-g', '--gpu', type=str, default="none", help='enter in the GPU type {V100, P100}')
parser.add_argument('-b', '--batch', nargs='+', type=int)
parser.add_argument('-n', '--nrequests', nargs='+',type=int)
parser.add_argument('-c', '--concurrency', nargs='+', type=int)
parser.add_argument('--ngpus', nargs='+', type=int)
parser.add_argument('-p', '--ports',  nargs='+', type=int)
parser.add_argument('-o', '--outfn', default='results.csv')
parser.add_argument('-m', '--model', nargs='+', type=str)
parser.add_argument('-a', '--algorithm', default='tfs_grpc_client.py')
parser.add_argument('-y', '--config', type=str)
args = parser.parse_args()

with open (args.outfn, 'w') as csvfile:
    cw = csv.writer(csvfile, delimiter=',')
    cw.writerow("Timestamp:GPU:# of GPUs:Server:Concurrency:Model:# of Requests:BatchSize:Theta (inf/s)".split(":"))
    # cw.writerow("Timestamp:GPU:# of GPUs:Server:Concurrency:Model:# of Requests:BatchSize:Throughput (inf/s):Theta (inf/s):Latency (ms)".split(":"))

extract = lambda x: float(re.findall('\d+.\d+', x)[0])

config_file = args.config
if ".yaml" in args.server:
    # read and parse YAML file
    config_file = args.server
    with open(args.server,'r') as f:
        sections = yaml.load(f.read(), Loader=yaml.FullLoader)

    for section, options in sections.items():
        for option, value in options.items():
            setattr(args, option, value)

print(args)

Shell.mkdir("results")
StopWatch.start("loop")

for model in args.model: # e.g. ["small_lstm","medium_cnn","large_tcnn"]
    print(f"\nmodel: {model}")
    for nrequests in args.nrequests: # e.g. [50,100]
        print(f"nrequests: {nrequests}")
        for batchsize in args.batch: # e.g. [16, 64]
            print(f"batchsize: {batchsize}")
            for ngpus in args.ngpus: # e.g. [1, 2, 4, 8]
                print(f"ngpus: {ngpus}")
                for concurrency in args.concurrency: # e.g. [1, 2, 4, 8, 16]
                    StopWatch.start(f"concurrency-{concurrency}")
                    start = time.perf_counter()
                    print(f"concurrency: {concurrency}")
                    proc = []
                    # filenames = []
                    for server_id, port in enumerate(args.ports[:ngpus], start=1): #[8500....8505]
                        for client_rank in range(concurrency):
                            cmd = f"python {args.algorithm} {args.server}:{port} -m {model} -b {batchsize} -n {nrequests}"
                            log_file = f"results/log-{model}-{nrequests}-{batchsize}-{ngpus}-{concurrency}-{server_id}-{port}-{client_rank}.txt"
                            # cmd = f"python {args.algorithm} {args.server}:{port} -m {model} -b {batchsize} -n {nrequests}" 
                            print(log_file)
                            timestamp = datetime.datetime.now().time()
                            print(timestamp, cmd)
                            f = open(log_file,"w")
                            process = subprocess.Popen(cmd, stdout=f,
                                                         stderr=subprocess.STDOUT,
                                                         shell=True)
                            assert not process.returncode, "client did not complete successfully"
                            proc.append(process)
                            # filenames.append(f"log{server_id}.{client_rank}.txt")

                    # Barrier 
                    exit_codes = [p.wait() for p in proc]
                    
                    t_concurrency = time.perf_counter() - start
                    StopWatch.stop(f"concurrency-{concurrency}")

                    filenames = glob.glob(os.path.join(out_path, "results/log*"))
                    print(filenames)
                    num_files = len(filenames)
                    throughput = latency = 0

                    for fn in filenames:
                        with open(fn) as f:
                            lines = f.readlines()

                        # for line in lines:
                        #     if re.search("throughput:", line): throughput += extract(line)
                        #     if re.search("latency:", line): latency += extract(line)
                        
                        # Delete log files after getting perf metrics.
                        os.unlink(fn)

                    # total throughput in samples per second - see Brewer et. al (2021) equation 1
                    theta = nrequests*batchsize*concurrency/t_concurrency
                    # avg_latency = latency/num_files
                    # print(f"\nthroughput: {throughput:.2f}")
                    print(f"theta: {theta:.2f}") 
                    # print(f"avg latency: {avg_latency:.2f}")
                    StopWatch.event("metabench result", {"theta": theta,# "throughput": throughput, "avg latency": avg_latency,
                                                         "model": model, "number of requests": nrequests, "batchsize": batchsize,
                                                         "ngpus": ngpus, "concurrency": concurrency, "config file": config_file})
                    with open(args.outfn, 'a') as csvfile:
                        cw = csv.writer(csvfile, delimiter=',')
                        cw.writerow([timestamp, args.gpu, ngpus, server_id, concurrency, model, nrequests, batchsize, theta])    
                        # cw.writerow([timestamp, args.gpu, server_id, concurrency, model, nrequests, batchsize, throughput, theta, avg_latency])    
StopWatch.stop("loop")
StopWatch.benchmark()
StopWatch.benchmark(filename=f"metabench-{args.config}.log")
