"""
Client

Usage:
  Client.py run -c <config> | --config=<config> [-s <server>] [-p <port>] [-b <batch>] [-m <model>] [-n <nrequests>] [-o <osmi_sif>] [-a <algorithm>] [--concurrency <concurrency>] [--output_dir=<output_dir>]
  Client.py (-h | --help)

Options:
  -h --help                             Show this screen.
  -c <config> --config=<config>         Model config file.
  -s <server> --server=<server>         Server IP, e.g. 10.1.1.37.
  -p <port> --port=<port>               Server port, e.g. 8443.
  -b <batch> --batch=<batch>            Batch size.
  -m <model> --model=<model>            Model name, e.g. small_lstm].
  -n <nrequests> --nrequests=<nrequests> Number of requests.
  -o <osmi_sif> --osmi_sif=<osmi_sif>   OSMI singularity image.
  -a <algorithm> --algorithm=<algorithm> Client program.
  --output_dir=<output_dir>             Output directory.
"""

from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
import time
import requests
from docopt import docopt
import os
from cloudmesh.common.FlatDict import FlatDict
from multiprocessing import Process

args = docopt(__doc__)

config = FlatDict()
config.load(args["--config"] or "config.yaml", expand=True)

arg_to_config_mapping = {
    "--server": "constant.server",
    "--port": "constant.haproxy_port",
    "--batch": "experiment.batch",
    "--model": "experiment.model",
    "--nrequests": "constant.nrequests",
    "--osmi_sif": "data.sif_dir",
    "--algorithm": "constant.algorithm",
    "--output_dir": "data.output",
    "--concurrency": "experiment.concurrency"
}

for arg_key, config_key in arg_to_config_mapping.items():
    if args[arg_key]:
        config[config_key] = args[arg_key]

config["experiment.concurrency"] = int(config["experiment.concurrency"])

SINGULARITY = "singularity exec --bind `pwd`:/home --pwd /home"

class OSMI:

    def __init__(self, config):
        self.model = config["experiment.model"]
        self.nrequests = config["constant.nrequests"]
        self.batch = config["experiment.batch"]
        self.server = config["constant.server"]
        self.port = config["constant.haproxy_port"]
        self.osmi_sif = config["data.osmi_sif"]
        self.algorithm = config["constant.algorithm"]
        self.output_dir = config["data.output"]
        # self.log_file = f"{self.output_dir}/log-{self.model}-{self.nrequests}-{self.batch}-{self.port}.txt"

    def run(self, id):
        log_file = f"{self.output_dir}/log-{id}-{self.model}-{self.nrequests}-{self.batch}-{self.port}.txt"
        cmd = f"time {SINGULARITY} {self.osmi_sif} "\
              f"python {self.algorithm} {self.server}:{self.port} -m {self.model} -b {self.batch} -n {self.nrequests} &> {log_file}"
        print(cmd)
        r = os.system(cmd)
        print(r)

if __name__ == "__main__":
    osmi = OSMI(config)
    StopWatch.start("wrapper-total")
    processes = []
    for idx in range(config["experiment.concurrency"]):
        p = Process(target=osmi.run, args=(idx,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    StopWatch.stop("wrapper-total")
    # result = {
    #     "model": config["experiment.model"],
    #     "nrequests": config["constant.nrequests"],
    #     "batch": config["experiment.batch"],
    #     "algorithm": config["constant.algorithm"],
    #     "concurrency": config["experiment.concurrency"],
    # }
    # StopWatch.event("client result", {"latency": avg_inference_latency, "throughput": throughput})
    StopWatch.benchmark(sysinfo=False, csv=True)