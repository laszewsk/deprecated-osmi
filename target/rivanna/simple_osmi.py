from cloudmesh.common.Shell import Shell
import time
import requests
# from docopt import docopt
import argparse
import os
from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.FlatDict import expand_config_parameters

parser = argparse.ArgumentParser()
parser.add_argument('-s', 'server', help='server ip, e.g. 10.1.1.37')
parser.add_argument('-p', '--port', type=int, help='server port, e.g. 8443')
parser.add_argument('-b', '--batch', type=int, help='batch size')
parser.add_argument('-m', '--model', required=True, type=str, help='model name, e.g. small_lstm')
parser.add_argument('-n', '--nrequests', type=int, help='number of requests')
parser.add_argument("-c", "--config", type=str, required=True, help="model config file")
args = parser.parse_args()

config = FlatDict()
config.load(getattr(args,'config'), expand=True)

config["experiment.batch"] = int(config["experiment.batch"])
# config["experiment.repeat"] = int(config["experiment.repeat"])
# config["experiment.concurrency"] = int(config["experiment.concurrency"])

arg_to_config_mapping = {
    "server": "constant.server",
    "port": "constant.haproxy_port",
    "batch": "experiment.batch",
    "model": "experiment.model",
    "nrequests": "constant.nrequests",
    "sif_dir": "data.sif_dir",
}

for arg_key, config_key in arg_to_config_mapping.items():
    arg_value = getattr(args, arg_key)
    if arg_value is not None:
        config[config_key] = arg_value

SINGULARITY = "singularity exec --bind `pwd`:/home --pwd /home"

class OSMI:

    def __init__(self, config):
        self.model = config["experiment.model"]
        self.nrequests = config["constant.nrequests"]
        self.batch = config["experiment.batch"]
        self.server = config["constant.server"]
        self.port = config["constant.haproxy_port"]
        self.osmi_sif = config["data.osmi_sif"]
        self.log_file = f"results/log-{self.model}-{self.nrequests}-{self.batch}-{self.server_id}-{self.port}.txt"

    def run(self):
        cmd = f"time {SINGULARITY} {self.osmi_sif} "\
              f"python {self.algorithm} {self.server}:{self.port} -m {self.model} -b {self.batch} -n {self.nrequests} &> {self.log_file}"
        print(cmd)
        r = os.system(cmd)
        print(r)


# def osmi(args):
#     log_file = f"results/log-{args.model}-{args.nrequests}-{args.batchsize}-{args.ngpus}-{args.concurrency}-{args.server_id}-{args.port}.txt"
#     Shell.run(f"python {args.algorithm} {args.server}:{args.port} -m {args.model} -b {args.batchsize} -n {args.nrequests} > {log_file}") 

if __name__ == "__main__":
    # with open(args.config) as stream:
    #     config = yaml.safe_load(stream)
    # osmi(config)
    osmi = OSMI(config)
    osmi.run()
