"""
LoadBalancer

Usage:
  LoadBalancer.py start_and_wait [-c <config> | --config=<config>] [-p <port> | --haproxy_port=<port>] [-o <output> | --output_dir=<output>] [-s <image> | --haproxy_sif=<image>] [--timeout=<timeout>] [--tfs_base_port=<port>] [--ngpus=<ngpus>] [--haproxy_cfg_file=<haproxy_cfg_file>] [--server=<server>]
  LoadBalancer.py start [-c <config> | --config=<config>] [-p <port> | --haproxy_port=<port>] [-o <output> | --output_dir=<output>] [-s <image> | --haproxy_sif=<image>]
  LoadBalancer.py wait [-c <config> | --config=<config>]
  LoadBalancer.py (-h | --help)

Options:
  -h --help                         Show this screen.
  -c <config> --config=<config>     Model config file.
  -p <port> --haproxy_port=<port>   Port for haproxy server.
  -o <output> --output_dir=<output> Directory to store output logs.
  -s <image> --haproxy_sif=<image>  HAProxy singularity image.
"""

from cloudmesh.common.Shell import Shell
import time
from docopt import docopt
import os
import socket
from cloudmesh.common.FlatDict import FlatDict
from pprint import pprint
from haproxy_cfg_generator import generate_haproxy_cfg
from port_generator import unique_base_port

SINGULARITY = "singularity exec --bind `pwd`:/home --pwd /home"

class HAProxyLoadBalancer:

    def __init__(self, config):
        self.port = unique_base_port(config)
        self.output_dir = config["data.output"]
        generate_haproxy_cfg(config)
        self.haproxy_config_file = config["data.haproxy_cfg_file"]
        self.haproxy_sif = config["data.haproxy_sif"]

    def start(self):
        command = f"time {SINGULARITY} {self.haproxy_sif} " \
                  f"haproxy -d -f {self.haproxy_config_file} >& {self.output_dir}/haproxy.log &"
        print(command)
        r = os.system(command)
        print(r)

    def shutdown(self):
        raise NotImplementedError

    def status(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', port)) == 0

    def wait_for_server(self):
        start = time.time()
        while not self.status(self.port):
            if time.time() - start > 45:
                raise ValueError("Load balancer not properly started")
            time.sleep(0.5)
            print(".", end="")
        print()


def main():
    args = docopt(__doc__)

    config_file = args["--config"] or "config.yaml"
    config = FlatDict()
    config.load(config_file, expand=True)

    arg_to_config_mapping = {
        "--haproxy_port": "constant.haproxy_port",
        "--haproxy_sif": "data.haproxy_sif",
        "--output_dir": "data.output",
        "--tfs_base_port": "constant.tfs_base_port",
        "--ngpus": "experiment.ngpus",
        "--haproxy_cfg_file": "data.haproxy_cfg_file",
        "--server": "constant.server",
    }

    for arg_key, config_key in arg_to_config_mapping.items():
        if args[arg_key]:
            config[config_key] = args[arg_key]

    config["experiment.ngpus"] = int(config["experiment.ngpus"])

    load_balancer = HAProxyLoadBalancer(config)
    if args["start"]:
        load_balancer.start()
    elif args["wait"]:
        load_balancer.wait_for_server()
    elif args["start_and_wait"]:
        load_balancer.start()
        load_balancer.wait_for_server()

if __name__ == '__main__':
    main()