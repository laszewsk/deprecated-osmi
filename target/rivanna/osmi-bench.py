from cloudmesh.common.Shell import Shell
import time
import requests
# from docopt import docopt
import argparse
import os
from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.FlatDict import expand_config_parameters
from ModelServer import ModelServer
from LoadBalancer import HAProxyLoadBalancer
from simple_osmi import OSMI

parser = argparse.ArgumentParser()
parser.add_argument('-s', 'server', help='server ip, e.g. 10.1.1.37')
parser.add_argument('-b', '--batch', type=int, help='batch size')
parser.add_argument('-m', '--model', type=str, help='model name, e.g. small_lstm')
parser.add_argument('-n', '--nrequests', type=int, help='number of requests')
parser.add_argument("-h", "--haproxy_port", type=int, help="port for haproxy server")
parser.add_argument("-o", "--output_dir", type=str, help="directory to store output logs")
parser.add_argument("-c", "--config", type=str, help="model config file")
parser.add_argument("-t", "--tfs_base_port", type=int, help="base port for TF servers")
parser.add_argument("-g", "--ngpus", type=int, help="number of GPUs")
# ap.add_argument("-m", "--model_conf_base_name", type=str, required=False, help="model config file base name")
args = parser.parse_args()

config = FlatDict()
config.load(getattr(args, 'config'), expand=True)

config["experiment.ngpus"] = int(config["experiment.ngpus"])
config["experiment.batch"] = int(config["experiment.batch"])
# config["experiment.repeat"] = int(config["experiment.repeat"])
# config["experiment.concurrency"] = int(config["experiment.concurrency"])

arg_to_config_mapping = {
    "server": "constant.server",
    "haproxy_port": "constant.haproxy_port",
    "batch": "experiment.batch",
    "model": "experiment.model",
    "nrequests": "constant.nrequests",
    "tfs_base_port": "constant.tfs_base_port",
    "ngpus": "experiment.ngpus",
    "output_dir": "data.output",
}

for arg_key, config_key in arg_to_config_mapping.items():
    arg_value = getattr(args, arg_key)
    if arg_value is not None:
        config[config_key] = arg_value

model_server = ModelServer(config)
model_server.start()
model_server.waiter_for_server()

load_balancer = HAProxyLoadBalancer(config)
load_balancer.start()
load_balancer.wait_for_server()

osmi = OSMI(config)
osmi.run()
