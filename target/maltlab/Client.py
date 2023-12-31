"""
Client

Usage:
  Client.py run --config=CONFIG
                [--server=SERVER]
                [--port=PORT]
                [--batch=BATCH]
                [--model=MODEL]
                [--nrequests=REQUESTS]
                [--osmi_sif=OSMI_SIF]
                [--algorithm=ALGORITHM]
                [--concurrency=CONCURRENCY]
                [--output_dir=OUTPUT_DIR]
  Client.py (-h | --help)

Options:
  -h --help                Manaual page.
  --config=CONFIG          Model config file [default: config.yaml].
  --server=SERVER          Server IP, e.g. 10.1.1.37.
  --port=PORT              Server port, e.g. 8443.
  --batch=BATCH            Batch size.
  --model=MODEL            Model name, e.g. small_lstm].
  --nrequests=REQUESTS     Number of requests.
  --osmi_sif=OSMI_SIF      OSMI singularity image.
  --algorithm=ALGORITHM    Client program.
  --output_dir=OUTPUT_DIR  Output directory.
"""

from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
import time
import requests
from docopt import docopt
import os
from cloudmesh.common.FlatDict import FlatDict
from multiprocessing import Process
from port_generator import unique_base_port
# from cloudmesh.common.network import PortGenerator

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
        # p = PortGenerator(2500)
        # self.port = p.get_port()
        self.port = unique_base_port(config)
        self.osmi_sif = config["data.osmi_sif"]
        self.algorithm = config["constant.algorithm"]
        self.output_dir = config["data.output"]
        # self.log_file = f"{self.output_dir}/log-{self.model}-{self.nrequests}-{self.batch}-{self.port}.txt"

    def run(self, id):
        log_file = f"{self.output_dir}/log-{id}-{self.model}-{self.nrequests}-{self.batch}-{self.port:04d}.txt"
        cmd = f"time {SINGULARITY} {self.osmi_sif} "\
              f"python {self.algorithm} {self.server}:{self.port:04d} -m {self.model} -b {self.batch} -n {self.nrequests} --identifier {id} &> {log_file}"
        
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
